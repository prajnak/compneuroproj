function [net, info] = cnn_emotion(varargin)
% nmost, prajnak, rootmeansquare, adopted from MatConvNet examples

run('vl_setupnn') %wherever this is located on your computer

opts.batchNormalization = false ;
opts.networkType = 'simplenn' ;
[opts, varargin] = vl_argparse(opts, varargin) ;

sfx = opts.networkType ;
if opts.batchNormalization, sfx = [sfx '-bnorm'] ; end
opts.expDir = fullfile(vl_rootnn, 'data', ['emotion-baseline' sfx]) ;
[opts, varargin] = vl_argparse(opts, varargin) ;

opts.train = struct() ;
opts = vl_argparse(opts, varargin) ;
if ~isfield(opts.train, 'gpus'), opts.train.gpus = []; end;

% --------------------------------------------------------------------
%                                                         Prepare data
% --------------------------------------------------------------------

net = cnn_emotion_init('batchNormalization', opts.batchNormalization, ...
                     'networkType', opts.networkType) ;

imdb = load('imdb.mat') ;
deviation_data = bsxfun(@minus, imdb.images.data, imdb.images.data_mean);
% imdb.images.data = deviation_data;
imdb.images.data = gpuArray(deviation_data);
imdb.images.data_mean = gpuArray(imdb.images.data_mean);
imdb.images.labels = gpuArray(imdb.images.labels);
imdb.images.set = gpuArray(imdb.images.set);


net.meta.classes.name = arrayfun(@(x)sprintf('%d',x),1:10,'UniformOutput',false) ;

% --------------------------------------------------------------------
%                                                                Train
% --------------------------------------------------------------------

switch opts.networkType
  case 'simplenn', trainfn = @cnn_train ;
  case 'dagnn', trainfn = @cnn_train_dag ;
end

[net, info] = trainfn(net, imdb, getBatch(opts), ...
  'expDir', opts.expDir, ...
  net.meta.trainOpts, ...
  opts.train, ...
  'val', find(imdb.images.set == 3)) ;

% --------------------------------------------------------------------
function fn = getBatch(opts)
% --------------------------------------------------------------------
switch lower(opts.networkType)
  case 'simplenn'
    fn = @(x,y) getSimpleNNBatch(x,y) ;
  case 'dagnn'
    bopts = struct('numGpus', numel(opts.train.gpus)) ;
    fn = @(x,y) getDagNNBatch(bopts,x,y) ;
end

% --------------------------------------------------------------------
function [images, labels] = getSimpleNNBatch(imdb, batch)
% --------------------------------------------------------------------
images = imdb.images.data(:,:,:,batch) ;
labels = imdb.images.labels(1,batch) ;

% --------------------------------------------------------------------
% function inputs = getDagNNBatch(opts, imdb, batch)
% % --------------------------------------------------------------------
% images = imdb.images.data(:,:,batch) ;
% labels = imdb.images.labels(1,batch) ;
% if opts.numGpus > 0
%   images = gpuArray(images) ;
% end
% inputs = {'input', images, 'label', labels} ;
% 
% 
% set = [ones(1,numel(y1)) 3*ones(1,numel(y2))];
% data = single(reshape(cat(3, x1, x2),160,160,1,[]));
% dataMean = mean(data(:,:,set == 1), 4);
% data = bsxfun(@minus, data, dataMean) ;
% 
% imdb.images.data = data ;
% imdb.images.data_mean = dataMean;
% imdb.images.labels = cat(2, y1, y2) ;
% imdb.images.set = set ;
% imdb.meta.sets = {'train', 'val', 'test'} ;
% imdb.meta.classes = arrayfun(@(x)sprintf('%d',x),0:9,'uniformoutput',false) ;
