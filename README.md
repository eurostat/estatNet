CONetStat
=========

Module for Eurostat online glossaries' web scraping, ontology indexing and semantic classification
---

**About**

This module will enable you to automatically scrape _Eurostat_ so-called  _"Statistics Explained_" and index the contents of those pages. It will build a graph of inter-relationships between the pages while extracting some semantic contents ("concepts"). The interconnected concepts are then used to automatically train a text classifier.

<table align="center">
    <tr> <td align="left"><i>documentation</i></td> <td align="left">available at: https://gjacopo.github.io/esscrape/</td> </tr> 
    <tr> <td align="left"><i>since</i></td> <td align="left">2018</td> </tr> 
    <tr> <td align="left"><i>license</i></td> <td align="left"><a href="https://joinup.ec.europa.eu/sites/default/files/eupl1.1.-licence-en_0.pdfEUPL">EUPL</a> </td> </tr> 
</table>


**<a name="Description"></a>Description**

**<a name="Notes"></a>Notes**

**<a name="Resources"></a>Resources**

* [`Keras`](https://keras.io), the `Python` Deep Learning library.
* Various algorithms for short text categorization: [`PyShortTextCategorization`](https://github.com/stephenhky/PyShortTextCategorization).
* Source code for large-scale hierarchical text classification with recursively regularized Deep Graph-CNN: [`Deepgraphcnn`](https://github.com/HKUST-KnowComp/DeepGraphCNNforTexts).
* Convolutional Neural Networks for sentence classification: [`CNN_sentence`](https://github.com/yoonkim/CNN_sentence).
* Tool [`word2vec`](https://code.google.com/archive/p/word2vec/) for computing continuous distributed representations of words, with pre-trained word and phrase vectors; see also [mirror repository](https://github.com/mmihaltz/word2vec-GoogleNews-vectors).
* [Implementation of Graph Convolutional Networks](https://github.com/tkipf/gcn) in [`TensorFlow`](https://www.tensorflow.org).
* Text matching toolkit [`MatchZoo`](https://github.com/faneshion/MatchZoo) for designing, comparing, and sharing of deep text matching models.
* Britz D. [blog](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/) on implementing a Convolutional Neural Network for text classification in `Tensorflow` and [source code `cnn-text-classification-tf`](https://github.com/dennybritz/cnn-text-classification-tf).
* Britz D. [blog](http://www.wildml.com/2015/11/understanding-convolutional-neural-networks-for-nlp/) for understanding Convolutional Neural Networks for NLP.
* Kipf T.N. [blog](https://tkipf.github.io/graph-convolutional-networks/) on Graph Convolutional Network.
* Framework [`Scrapy`](https://scrapy.org) for extracting data from online websites.
* Natural language toolkit [`nltk`](http://www.nltk.org/) to work with human language data.
* Package [`NetworkX`](https://networkx.github.io/) for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* Module [`py2neo`](http://py2neo.org/v3/) for [`neo4j`](https://neo4j.com/) graph database, though the bolt driver [`neo4j-python-driver`](https://github.com/neo4j/neo4j-python-driver) does the job.

**<a name="References"></a>References**

* Peng H., Li J., He Y., Liu Y., Bao M., Song Y., and Yang Q. (2018): [**Large-scale hierarchical text classification with recursively regularized Deep Graph-CNN**](http://www.cse.ust.hk/~yqsong/papers/2018-WWW-Text-GraphCNN.pdf), Proc. _WWW_.
* Yu J., Lu Y., Qin Z., Liu Y., Tan J., Guo L., and Zhang W. (2018): [**Modeling text with Graph Convolutional Network for cross-modal information retrieval**](https://arxiv.org/pdf/1802.00985.pdf), arXiv:[1802.00985](https://arxiv.org/abs/1802.00985).
* Wang T., Wu D.J., Coates A., and Ng, A.Y. (2018): [**End-to-end text recognition with Convolutional Neural Networks**](https://crypto.stanford.edu/~dwu4/papers/TextRecogCNN.pdf).
* Schlichtkrull M., Kipf T.N., Bloem P., van den Berg R., Titov I., and Welling M. (2018): [**Modeling relational data with Graph Convolutional Networks**](https://arxiv.org/pdf/1703.06103.pdf), Proc. _ESWC_, arXiv:[1703.06103](https://arxiv.org/abs/1703.06103).
* Zhang Z., Robinson D., and  Tepper J. (2018): [**Detecting hate speech on Twitter using a Convolution-GRU based Deep Neural Network**](https://2018.eswc-conferences.org/wp-content/uploads/2018/02/ESWC2018_paper_48.pdf), Proc. _ESWC_.
* Liu B., Zhang T., Niu D., Lin J., Lai K., and Xu Y. (2018): [**Matching long text documents via Graph Convolutional Networks**](https://arxiv.org/pdf/1802.07459.pdf), arXiv:[1802.07459](https://arxiv.org/abs/1802.07459).
* Kipf T.N. and Welling M. (2017) [**Semi-supervised classification with Graph Convolutional Networks**](https://arxiv.org/pdf/1609.02907.pdf), Proc. _ ICLR_, arXiv:[1609.02907](https://arxiv.org/abs/1609.02907).
* Fan Y., Pang L.,  Hou J.P., Guo J., Lan Y., and Cheng X. (2017): [**MatchZoo: A toolkit for deep text matching**](https://arxiv.org/pdf/1707.07270.pdf), Proc. _SIGIR_, arXiv:[1707.07270](https://arxiv.org/abs/1707.07270).
* Mitra B., Diaz F., and Craswell N. (2017): [**Learning to match using local and distributed representations of text for web search**](https://arxiv.org/pdf/1610.08136.pdf), Proc. _ICWWW_, arXiv:[1610.08136](https://arxiv.org/abs/1610.08136).
* Defferrard M., Bresson X. and Vandergheynst P. (2016): [**Convolutional Neural Networks on graphs with fast localized spectral filtering**](https://arxiv.org/pdf/1606.09375), Proc. _NIPS_, arXiv:[1606.09375](https://arxiv.org/abs/1606.09375).
* Zhang X., Zhao J., and LeCun Y. (2015): [**Character-level Convolutional Networks for text classification**](https://arxiv.org/pdf/1509.01626.pdf), Proc. _NIPS_, arXiv:[1509.01626](https://arxiv.org/abs/1509.01626).
* Johnson R. and Zhang T. (2015): [**Semi-supervised Convolutional Neural Networks for text categorization via region embedding**](https://arxiv.org/pdf/1504.01255.pdf), arXiv:[1504.01255](https://arxiv.org/abs/1504.01255).
* Qiu, X. and Huang, X. (2015): [**Convolutional Neural Tensor Network architecture for community-based question answering**](https://www.ijcai.org/Proceedings/15/Papers/188.pdf), Proc. _IJCAI_.
* Wang P., Xu J., Xu B., Liu C., Zhang H., Wang F., and Hao H. (2015): [**Semantic clustering and Convolutional Neural Network for short text categorization**](http://www.aclweb.org/anthology/P15-2058), doi:10.3115/v1/P15-2058. 
* Kim Y. (2014): [**Convolutional Neural Networks for sentence classification**](https://arxiv.org/pdf/1408.5882.pdf), arXiv:[1408.5882](https://arxiv.org/abs/1408.5882).
