import torch
from torch import nn


def save_model(
    model,
    save_dir,
    epoch=0,
    optimizer=None,
    loss=None,
):
    if isinstance(model, nn.DataParallel):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    if optimizer is None:
        optim_params = None
    else:
        optim_params = optimizer.state_dict()
    torch.save(
        {
            'init_args': model.init_args,
            'epoch': epoch,
            'model_state_dict': state_dict,
            'optimizer_state_dict': optim_params,
            'loss': loss,
        },
        save_dir
    )


def load_model(
    save_dir,
    model_class=None,
    model=None,
    optimizer=None,
    train=False,
):
    # from .model_dict import MODEL_DICT
    checkpoint = torch.load(save_dir)
    if model is None:
        init_args = checkpoint['init_args']
        assert model_class is not None
        model = model_class(**init_args)
        model.load_state_dict( 
            checkpoint['model_state_dict'], 
        )
    
    elif isinstance(model, nn.DataParallel):
        state_dict = checkpoint['model_state_dict']
        from collections import OrderedDict
        new_state_dict = OrderedDict()

        for k, v in state_dict.items():
            if 'module' not in k:
                k = 'module.' + k
            else:
                k = k.replace('features.module.', 'module.features.')
            new_state_dict[k] = v
        model.load_state_dict(new_state_dict)
    else:
        model.load_state_dict( 
            checkpoint['model_state_dict'], 
        )
    
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']

    if train:
        model.train()
    else:
        model.eval()

    return model, optimizer, epoch, loss