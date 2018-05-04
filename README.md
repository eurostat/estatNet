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

* [Implementation of Graph Convolutional Networks](https://github.com/tkipf/gcn) in [TensorFlow]().
* Text matching toolkit [MatchZoo](https://github.com/faneshion/MatchZoo) for designing, comparing, and sharing of deep text matching models.
* Framework [_Scrapy_](https://scrapy.org) for extracting data from online websites.
* Natural language toolkit [_nltk_](http://www.nltk.org/) to work with human language data.
* Package [_NetworkX_](https://networkx.github.io/) for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* Module [_py2neo_](http://py2neo.org/v3/) for [_neo4j_](https://neo4j.com/) graph database, though the bolt driver [_neo4j-python-driver_](https://github.com/neo4j/neo4j-python-driver) does the job.

**<a name="References"></a>References**

* Liu B., Zhang T., Niu D., Lin J., Lai K., and Xu Y. (2018): [**Matching long text documents via Graph Convolutional Networks**](https://arxiv.org/pdf/1802.07459.pdf), arXiv:[1802.07459](https://arxiv.org/abs/1802.07459).
* Kipf T. and Welling M. (2017) [**Semi-supervised classification with Graph Convolutional Networks**](https://arxiv.org/pdf/1609.02907.pdf), Proc. _ ICLR_, arXiv:[1609.02907](https://arxiv.org/abs/1609.02907).
* Fan Y., Pang L.,  Hou J.P., Guo J., Lan Y., and Cheng X. (2017): [**MatchZoo: A toolkit for deep text matching**](https://arxiv.org/pdf/1707.07270.pdf), Proc. _SIGIR_, arXiv:[1707.07270](https://arxiv.org/abs/1707.07270).
* Kipf T. blog on [Graph Convolutional Network](https://tkipf.github.io/graph-convolutional-networks/).
* Mitra B., Diaz F., and Craswell N. (2017): [**Learning to match using local and distributed representations of text for web search**](https://arxiv.org/pdf/1610.08136.pdf), Proc. _ICWWW_, arXiv:[1610.08136](https://arxiv.org/abs/1610.08136).
* Defferrard M., Bresson X. and Vandergheynst P. (2016): [**Convolutional Neural Networks on graphs with fast localized spectral filtering**](https://arxiv.org/pdf/1606.09375), Proc. _NIPS_, arXiv:[1606.09375](https://arxiv.org/abs/1606.09375).
* Qiu, X. and Huang, X. (2015): [**Convolutional Neural Tensor Network architecture for community-based question answering**](https://www.ijcai.org/Proceedings/15/Papers/188.pdf), Proc. _IJCAI_. 
