# EEBO-verse

The repository host code and data for paper: `EEBO-Verse: Sifting for Poetry in Large Early Modern Corpora Using Visual Features`. 

If you are interested in our project and would like to get help from us, please feel free to contact us via `danlu@ucsd.edu` or create an issue to this respository!


## Dataset

There are two parts of the data: the image and the annotation. Due to a copyright issue, we do not directly share the original resolution of the EEBO image dump to the public. However, if you are affiliated with a university or institution that has a subscription to [EEBO (Early English Books Online)](https://about.proquest.com/en/products-services/eebo/), please contact me directly to obtain a copy of the image dump or you can contact your libiary to obtain a copy of it. 


#### TCP raw data

According to EEBO-TCP's [navigation page](https://textcreationpartnership.org/tcp-texts/eebo-tcp-collections-navigations/), you can: 
 - download indiviual xml file for each book from [here](https://github.com/Text-Creation-Partnership/EEBO-TCP-Collections-Navigations)
 - download the whole set from the public folder via [dropbox](https://www.dropbox.com/sh/pfx619wnjdck2lj/AAAeQjd_dv29oPymNoKJWfEYa?dl=0)

## Poetry text

For humanities researchers who are only interested in poetry text, we create a simply text dump here, via [google drive](https://drive.google.com/drive/u/3/folders/1WvKKMU0kE2h5yDRfgChIGSOwgCoqpeNp). The script to process the xml file to obtain poetry only text is available [here](https://gist.github.com/taineleau/d123ca95d9da4abe58c789040d4790e3). We will released the poetry text we detected in the unannotated portion of EEBO later this year.


### Citing the paper

If you found the repository helpful to your research, please cite our paper and/or the EEBO/TCP project:

```
@inproceedings{chen2023eebo,
  title={EEBO-Verse: Sifting for Poetry in Large Early Modern Corpora Using Visual Features},
  author={Chen, Danlu and Jiang, Nan and Berg-Kirkpatrick, Taylor},
  booktitle={International Conference on Document Analysis and Recognition},
  pages={36--52},
  year={2023},
  organization={Springer}
}
````

