# %% [code]
import torch
from torch.utils.tensorboard import SummaryWriter
import torch.optim 
from datetime import datetime

REPORT_FREQUENCY = 100

def TrainModel(model, EPOCHS, loss_fn, train_loader, val_loader, optimizer, lr_scheduler, scaler = None):
    """
    This function will train your model and save the one that perfroms the best of validation data
    model: the model you wish to test
    EPOCHS: How many times you wish to train over the whole dataset
    loss_fn: your chose loss function
    train_loader: the data loader of the training dataset
    val_loader: the data loader of the Validation dataset
    optimizer: the algorthim to step toward the optimal solution
    lr_scheduler: the lr_scheduler changes the lr dynamically as needed
    scaler: scales the loss dues to our use of mixed precision
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    writer = SummaryWriter('{}runs/{}_{}'.format(model.path,model.name,timestamp))#used for tracking our model during training
    epoch_number = 0

    best_acc = 0.

    for epoch in range(EPOCHS):
        print('EPOCH {}:'.format(epoch_number + 1))

        # Make sure gradient tracking is on, and do a pass over the data
        model.train(True)
        avg_loss = train_one_epoch(model,train_loader,epoch_number, loss_fn, writer, optimizer,lr_scheduler,scaler)

        running_vloss = 0.0
        num_correct = 0
        num_samples = 0
        #now we eavluate on our validation set to perform early stopping
        model.eval()
        # Disable gradient computation and reduce memory consumption.
        with torch.no_grad():
            for i, vdata in enumerate(val_loader):
                vinputs, vtargets = vdata
                vinputs = vinputs.to(model.device)
                vtargets = vtargets.to(model.device)
                #again were using AMP to allow us to train faster
                #with torch.amp.autocast(torch.device(model.device).type):
                voutputs = model(vinputs)
                vloss = loss_fn(voutputs,vtargets)
                running_vloss += vloss
                _, preds = voutputs.max(1)
                _, vtarget = vtargets.max(1)
                num_correct += (preds == vtarget).sum()
                num_samples += preds.size(0)
        acc = float(num_correct) / num_samples

        avg_vloss = running_vloss / (i + 1)
        print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))
        print('Accuracy:', acc)
        # Log the running loss averaged per batch
        # for both training and validation
        writer.add_scalars('Training vs. Validation Loss',
                        { 'Training' : avg_loss, 'Validation' : avg_vloss },
                        epoch_number + 1)
        writer.add_scalar("Accuracy",acc,epoch_number+1)
        writer.flush()

        # Track best performance, and save the model's state
        #AKA early stopping, a form of regularization we talked about it class
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), "{}{}-Best".format(model.path,model.name))

        epoch_number += 1


def train_one_epoch(model, training_loader, epoch_index, loss_fn, tb_writer, optimizer, lr_scheduler, scaler= None):
    """
    This function will train your model and save the one that perfroms the best of validation data  
    model: the model you wish to test  
    train_loader: the data loader of the training dataset  
    epoch_index: what epoch we are in for reporting purposes  
    loss_fn: your chose loss function  
    tb_writer: a summaryWriter used for tracking our training  
    optimizer: the algorthim to step toward the optimal solution  
    lr_scheduler: the lr_scheduler changes the lr dynamically as needed  
    scaler: scales the loss dues to our use of mixed precision  
    """
    running_loss = 0.0
    last_loss = 0.0


     # progressively unfreeze blocks of Resnet (external: initially freeze all layers)
    start_freeze = 10
    interval = 10
    layer2 = True
    
    unfreeze_expand(model, optimizer, epoch_index, start_freeze, interval, layer2)

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        inputs, targets = data
        #send them to the model's device
        inputs = inputs.to(model.device)
        targets = targets.to(model.device)

        # Zero your gradients for every batch!
        optimizer.zero_grad()

        #use automatic mixed precision to reduce memory consumption and allow us to run on more limited resources
        #with torch.amp.autocast(torch.device(model.device).type):
            # Make predictions for this batch
        outputs = model(inputs)
            # Compute the loss and its gradients

        # resize targets to work with crossEntropyloss
        targets = targets.argmax(dim=1)
        
        loss = loss_fn(outputs,targets)
        running_loss += loss
        if scaler:#if were scaling our loss
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            old_scaler = scaler.get_scale()
            scaler.update()
            new_scaler = scaler.get_scale()
            if new_scaler >= old_scaler:
                lr_scheduler.step()
        else:
            loss.backward()
            optimizer.step()
            lr_scheduler.step()

        # Gather data and report
        
        if i % REPORT_FREQUENCY == REPORT_FREQUENCY-1:
            last_loss = running_loss / i # loss per batch
            print('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
    return last_loss

# ------------------------------#

def unfreeze_expand(model, optimizer, epoch, start_at_epoch, interval, layer2):

    lr = optimizer.param_groups[0]['lr']
    weight_decay = optimizer.param_groups[0]['weight_decay']
    
    # As epochs progress, gradually update which layers (in blocks) require gradient
    # Initially, froze all layers, first run is just fc layer gradient
    if epoch <= 0:
        for param in model.fc.parameters():
            param.requires_grad = True
    if epoch >= start_at_epoch:
        for param in model.layer4.parameters():
            param.requires_grad = True
    if epoch >= start_at_epoch + interval:
        for param in model.layer3.parameters():
            param.requires_grad = True
    if layer2:
        if epoch >= start_at_epoch + interval*2:
            for param in model.layer2.parameters():
                param.requires_grad = True

    # filter out layers that do NOT require gradient (requires_grad still = False)
    grad_params = filter(lambda p: p.requires_grad, model.parameters())
    # get dict of parameters requiring gradient
    grad_params_list = list(grad_params)
    grad_params_dict = {
                        'params': grad_params_list,
                        'lr': lr,
                        'weight_decay': weight_decay
                        }

    optimizer.add_param_group(grad_params_dict)

# -----------------------------#

def TestModel(model, test_loader,loss_fn):
    """
    This function will evaluate your model on the test dataset and report accuracy
    model: the model you wish to test
    test_loader: the dataloader of the testing dataset
    loss_fn: your chosen loss_function
    """
    model.eval()
    running_loss = 0.0
    num_correct = 0
    num_samples = 0
    # Disable gradient computation and reduce memory consumption.
    with torch.no_grad():
        for i, data in enumerate(test_loader):
            inputs, targets = data
            inputs = inputs.to(model.device)
            targets = targets.to(model.device)
            #get scores from the model
            scores = model(inputs)
            loss = loss_fn(scores,targets)
            running_loss += loss
            #get predication based off the maximum score
            _, preds = scores.max(1)
            _, target = targets.max(1)
            num_correct += (preds == target).sum()
            num_samples += preds.size(0)
        acc = float(num_correct) / num_samples
        print('Got %d / %d correct (%.2f)' % (num_correct, num_samples, 100 * acc))
    return acc
