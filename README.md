# cd4ml
Generic lib to enable CD4ML


## Graphs

In order to draw graphs it is necessary to install graphiz lib. Installation instructions can be found in pygraphviz website: https://pygraphviz.github.io/documentation/latest/install.html 

### MacOS

It can be challenging to install graphviz on Mac and let pip know about it. The following is a lista of common commands to get graphviz configuration:

* Install graphviz

```
brew install graphiz
```

* Need to find graphviz installed version

```
% brew info graphviz | grep graphviz:
graphviz: stable 3.0.0 (bottled), HEAD
```

* Get the version and use provide it to pip installer:
```
% export GRAPHVIZ_VERSION=3.0.0.
% pip install --global-option=build_ext \
              --global-option="-I/opt/homebrew/Cellar/graphviz/${GRAPHVIZ_VERSION}/include/" \      
              --global-option="-L/opt/homebrew/Cellar/graphviz/${GRAPHVIZ_VERSION}/lib/" \
              pygraphviz
```