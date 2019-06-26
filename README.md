CONetStat
=========

Module for Eurostat online glossaries' web scraping, ontology indexing and semantic classification
---

**About**

This module will enable you to automatically scrape _Eurostat_ online_"Statistics Explained_" and index the contents of these pages into some sort of _knowledge graph_. It will actually build a graph of inter-relationships between the pages while extracting existing semantic contents (documentation, concepts, glossary, ...). 

<table align="center">
    <tr> <td align="left"><i>documentation</i></td> <td align="left">available at: https://gjacopo.github.io/esscrape/</td> </tr> 
    <tr> <td align="left"><i>since</i></td> <td align="left">2018</td> </tr> 
    <tr> <td align="left"><i>license</i></td> <td align="left"><a href="https://joinup.ec.europa.eu/sites/default/files/eupl1.1.-licence-en_0.pdfEUPL">EUPL</a> </td> </tr> 
</table>


**<a name="Description"></a>Description**

**<a name="Notes"></a>Notes**

**<a name="Resources"></a>Resources**

* Framework [`Scrapy`](https://scrapy.org) for extracting data from online websites.
* Natural language toolkit [`nltk`](http://www.nltk.org/) to work with human language data.
* Package [`NetworkX`](https://networkx.github.io/) for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
* Module [`py2neo`](http://py2neo.org/v3/) for [`neo4j`](https://neo4j.com/) graph database, though the bolt driver [`neo4j-python-driver`](https://github.com/neo4j/neo4j-python-driver) does the job.

**<a name="References"></a>References**

* **Statistics Explained** [main page](https://ec.europa.eu/eurostat/statistics-explained/index.php/Main_Page).
* [**How Open Are Official Statistics?**](http://opendatawatch.com/monitoring-reporting/how-open-are-official-statistics/).
