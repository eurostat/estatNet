esscrape
=======

Module for web scraping and semantic indexing of Eurostat online glossaries.
---

**About**

This module will enable you to automatically scrape _Eurostat_ so-called  _"Statistics Explained_" and index the contents of those pages. It will build a graph of inter-relationships between the pages while extracting some semantic contents ("concepts").

<table align="center">
    <tr> <td align="left"><i>documentation</i></td> <td align="left">available at: https://gjacopo.github.io/esscrape/</td> </tr> 
    <tr> <td align="left"><i>since</i></td> <td align="left">2018</td> </tr> 
    <tr> <td align="left"><i>license</i></td> <td align="left"><a href="https://joinup.ec.europa.eu/sites/default/files/eupl1.1.-licence-en_0.pdfEUPL">EUPL</a> </td> </tr> 
</table>


**<a name="Description"></a>Description**

**<a name="Notes"></a>Notes**

**<a name="References"></a>References**

* Framework [_Scrapy_](https://scrapy.org) for extracting data from online websites.
* Natural language toolkit [_nltk_](http://www.nltk.org/) to work with human language data.
* Package [_NetworkX_](https://networkx.github.io/) for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* Module [_py2neo_](http://py2neo.org/v3/) for [_neo4j_](https://neo4j.com/) graph database, though the bolt driver [_neo4j-python-driver_](https://github.com/neo4j/neo4j-python-driver) does the job.
