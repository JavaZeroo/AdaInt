exp_name = 'fakeji'

custom_imports=dict(
    imports=['adaint'],
    allow_failed_imports=False)

# model settings
model = dict(
    type='AiLUT',
    n_ranks=3,
    n_vertices=33,
    en_adaint=True,
    en_adaint_share=False,
    backbone='tpami', # 'res18'
    pretrained=False,
    n_colors=3,
    sparse_factor=0.0001,
    smooth_factor=0,
    monotonicity_factor=10.0,
    recons_loss=dict(type='MSELoss', loss_weight=1.0, reduction='mean'))
# model training and testing settings
train_cfg = dict(n_fix_iters=4500*5)
test_cfg = dict(metrics=['PSNR'], crop_border=0)

# dataset settings
train_dataset_type = 'FiveK'
val_dataset_type = 'FiveK'

train_pipeline = [
    dict(
        type='LoadImageFromFile',
        io_backend='disk',
        key='lq',
        backend='pillow',
        channel_order='rgb'),
    dict(
        type='LoadImageFromFile',
        io_backend='disk',
        key='gt',
        backend='pillow',
        channel_order='rgb'),
    dict(type='RandomRatioCrop', keys=['lq', 'gt'], crop_ratio=(0.6, 1.0)),
    dict(type='Flip', keys=['lq', 'gt'], flip_ratio=0.5, direction='horizontal'),
    dict(type='RandomColorJitter', keys=['lq'], brightness=0.2, saturation=0.2),
    dict(type='FlexibleRescaleToZeroOne', keys=['lq', 'gt'], precision=32),
    dict(type='ImageToTensor', keys=['lq', 'gt']),
    dict(type='Collect', keys=['lq', 'gt'], meta_keys=['lq_path', 'gt_path'])
]

test_pipeline = [
    dict(
        type='LoadImageFromFile',
        io_backend='disk',
        key='lq',
        backend='pillow',
        channel_order='rgb'),
    dict(
        type='LoadImageFromFile',
        io_backend='disk',
        key='gt',
        backend='pillow',
        channel_order='rgb'),
    dict(type='FlexibleRescaleToZeroOne', keys=['lq', 'gt'], precision=32),
    dict(type='ImageToTensor', keys=['lq', 'gt']),
    dict(
        type='Collect',
        keys=['lq', 'gt'],
        meta_keys=['lq_path', 'gt_path'])
]

data = dict(
    workers_per_gpu=8,
    train_dataloader=dict(samples_per_gpu=1),
    val_dataloader=dict(samples_per_gpu=1),
    test_dataloader=dict(samples_per_gpu=1, workers_per_gpu=8),

    # train
    train=dict(
        type=train_dataset_type,
        dir_lq='/root/autodl-tmp/fakeji/data_gen/source',
        dir_gt='/root/autodl-tmp/fakeji/data_gen/target',
        ann_file='/root/autodl-tmp/fakeji/data_gen/train.txt',
        pipeline=train_pipeline,
        test_mode=False,
        filetmpl_lq='{}.png',
        filetmpl_gt='{}.png'),
    # val
    val=dict(
        type=val_dataset_type,
        dir_lq='/root/autodl-tmp/fakeji/data_gen/source',
        dir_gt='/root/autodl-tmp/fakeji/data_gen/target',
        ann_file='/root/autodl-tmp/fakeji/data_gen/test.txt',
        pipeline=test_pipeline,
        test_mode=True,
        filetmpl_lq='{}.png',
        filetmpl_gt='{}.png'),
    # test
    test=dict(
        type=val_dataset_type,
        dir_lq='/root/autodl-tmp/fakeji/data_gen/source',
        dir_gt='/root/autodl-tmp/fakeji/data_gen/target',
        ann_file='/root/autodl-tmp/fakeji/data_gen/test.txt',
        pipeline=test_pipeline,
        test_mode=True,
        filetmpl_lq='{}.png',
        filetmpl_gt='{}.png'),
)

# optimizer
optimizers = dict(
    type='Adam',
    lr=1e-6,
    weight_decay=0,
    betas=(0.9, 0.999),
    eps=1e-8,
    paramwise_cfg=dict(custom_keys={'adaint': dict(lr_mult=0.1)}))
lr_config = None

# learning policy
total_iters = 4500*300

checkpoint_config = dict(interval=4500, save_optimizer=True, by_epoch=False)
evaluation = dict(interval=4500, save_image=False)
log_config = dict(
    interval=300,
    hooks=[
        dict(type='TextLoggerHook', by_epoch=False),
    ])

visual_config = None

# runtime settings
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = f'./work_dirs/{exp_name}'
load_from = None
resume_from = None
workflow = [('train', 1)]
find_unused_parameters = True
