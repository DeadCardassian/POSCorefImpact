# JJ2NN in Coref

## Overview
This project investigates the impact of part-of-speech (POS) changes on the performance of a [deterministic coreference resolution system](https://nlp.stanford.edu/software/dcoref.html) (dcoref). Using the Stanford NLP pipeline and the [CoNLL-2011 dataset](https://conll.cemantix.org/2011/data.html), we specifically modify the POS tags to explore how nominal adjectives affects coreference resolution (coref) performance.

## Table of Contents
1. [Background](#background)<br>
   1.1 [The basic idea](#the-basic-idea)<br>
   1.2 [Coref tagger](#coref-tagger)<br>
   1.3 [Dataset](#dataset)
3. [Setups](#setups)
4. [Methodology](#methodology)
5. [Usage](#usage)
6. [Experimental Results](#experimental-results)
7. [Conclusion](#conclusion)
8. [Dependencies and Installation](#dependencies-and-installation)
9. [Acknowledgement](#acknowledgement)


## Background
### 1.1 The basic idea
This is a practice that originated from an idea of investigating nominal adjectives phenomenon. Nominal adjectives are adjectives that function as nouns in certain contexts. For instance, in the phrase "Education reform supports the gifted," the word "gifted" acts as a noun. However, most rule-based POS tagger tend to mark such words as JJ. It's a convention that probably began with the [Penn Treebank tagging guidelines](https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf) (1990) for convenience purpose: 

>Generic adjectives should be tagged as adjectives (JJ) and not as plural common nouns (NNS), even when they trigger subject-verb agreement, if they can be modified by adverbs."

**Therefore, this project means to investigate the impact of labeling these JJ as NN on POS based coref tagger.** Other downstream tasks will be studied as appropriate.

### 1.2 Coref tagger
This project uses [Stanford Deterministic Coreference Resolution System](https://nlp.stanford.edu/software/dcoref.shtml) as the coref tagger. This is a rule-based coref tagger, It implements the multi-pass sieve coreference method described in [Lee et al. (CoNLL Shared Task 2011)](https://nlp.stanford.edu/pubs/conllst2011-coref.pdf) and [Raghunathan et al. (EMNLP 2010)](https://nlp.stanford.edu/pubs/coreference-emnlp10.pdf). It requires inputs such as POS tags, parse trees, and so on.

### 1.3 Dataset
This project uses the [CoNLL-2011 Shared Task dataset](https://conll.cemantix.org/2011/data.html), which includes annotated coreference information. The development set is used to score the model's performance. CoNLL 2011 dataset is based on Ontonotes5.0, details [here](https://aclanthology.org/W11-1901/).

## Setups
This research is based on the [Stanford NLP](https://stanfordnlp.github.io/CoreNLP/) and [CoNLL 2011](https://conll.cemantix.org/2011/introduction.html) pipelines.

Setup steps:

1. Download [Ontonotes5.0](https://catalog.ldc.upenn.edu/LDC2013T19) (LDC account required).
2. Follow the [tutorial](https://conll.cemantix.org/2011/data.html) to download the CoNLL 2011 development dataset and use the corresponding script to convert .skel files to conll-format files.
3. [Download v8.01 scorer as instructed](https://conll.cemantix.org/2011/software.html).
4. Follow the [dcoref tutorial](https://nlp.stanford.edu/software/dcoref.shtml) to reproduce their CoNLL 2011 results. This project uses the following instruction: `java -cp "*" -Xmx8g edu.stanford.nlp.dcoref.SieveCoreferenceSystem -props coref.properties`. `coref.properties` is in the repository, you need to fill in the scorer and dataset path first, the comments give examples.

If you can reproduce the results in step 4, you have completed setups consistent with this project.
## Methodology
First, through some tests performed on dcoref, it is observed that its performance depends heavily on the parse (syntax) tree, especially the NP phrases within it. To maximize the relationship between POS and coreference, I eliminated the effect of the parse tree on dcoref by replacing all phrases with X (unclassifiable), excluding TOP and S, which significantly reduced the accuracy of dcoref, and replacing all phrases with FRAG showed similar results. 

After deactivating the parse tree, I used the rule-based JJ2NN algorithm developed by [Qi Lemeng](https://github.com/qilem) and I to update all the POS information in the dataset.

JJ2NN algorithm details: 

## Usage
If you haven't finished setups, finish setups first.

The dataset has the following structure: `.../conll-2011-dev.v2/conll-2011/v2/data/dev/data/english/annotations/...`  

**directory** refers to: `.../conll-2011/v2/data/dev`

**file_suffix** should be: `.v2_auto_conll`

Following process changes the dataset, so it should be backed up in advance.

Run `python conll_parse_modify.py directory file_suffix` to deactivate parse tree.

Run `python conll_pos_modify.py directory file_suffix` to execute JJ2NN algorithm.

Run `java -cp "*" -Xmx8g edu.stanford.nlp.dcoref.SieveCoreferenceSystem -props coref.properties` to see the result.

## Experimental Results
As shown in the table, the first row is the default result of dcoref on CoNLL 2011 dev set, the second row is the result after deactivating the parse tree, and the third row is the result of deactivating the parse tree and using the JJ2NN algorithm. The format of this table is consistent with the table on the [dcoref home page](https://nlp.stanford.edu/software/dcoref.html). The result of deactivating the parse tree dropped significantly compared to the default result, since dcoref relies on the information in the parse tree to predict the coreference. 

Taking result 2 as the baseline, it is found that after modifying the POS using JJ2NN algorithm, precision improves while recall remains unchanged or decreases, which leads to a slight increase in F1, with a amplitude of about 0.1%. Since we only modified 206/136,863 (0.15%) words in total (nominal adjectives are rare), **the small improvement in the model score illustrates the effectiveness of the JJ2NN algorithm, and shows that it is not linguistically reasonable to label adjectives with noun characteristics as JJ.**
<table>
  <tr>
    <th rowspan="2"> </th>
    <th colspan="3">MUC</th>
    <th colspan="3">B cubed</th>
    <th colspan="3">CEAF (M)</th>
    <th colspan="3">CEAF (E)</th>
    <th rowspan="2">Avg F1</th>
  </tr>
  <tr>
    <th>P</th>
    <th>R</th>
    <th>F1</th>
    <th>P</th>
    <th>R</th>
    <th>F1</th>
    <th>P</th>
    <th>R</th>
    <th>F1</th>
    <th>P</th>
    <th>R</th>
    <th>F1</th>
  </tr>
  <tr>
    <td>conllst2011 dev (1)</td>
    <td>62.06</td>
    <td>59.31</td>
    <td>60.65</td>
    <td>56.20</td>
    <td>48.55</td>
    <td>52.10</td>
    <td>58.00</td>
    <td>57.52</td>
    <td>57.76</td>
    <td>48.89</td>
    <td>53.47</td>
    <td>51.08</td>
    <td>54.61</td>
  </tr>
  <tr>
    <td>conll 2011 w/o parse tree (2) (baseline)</td>
    <td>58.31</td>
    <td>41.14</td>
    <td>48.24</td>
    <td>50.13</td>
    <td>31.22</td>
    <td>38.48</td>
    <td>57.42</td>
    <td>38.66</td>
    <td>46.21</td>
    <td>49.50</td>
    <td>28.87</td>
    <td>36.47</td>
    <td>41.06</td>
  </tr>
  <tr>
    <td>conll 2011 J2N w/o parse tree (3)</td>
    <td>58.42<br>(+0.19%↑)</span></td>
    <td>41.14</td>
    <td>48.28<br>(+0.08%↑)</span></td>
    <td>50.21<br>(+0.16%↑)</span></td>
    <td>31.22</td>
    <td>38.50<br>(+0.05%↑)</span></td>
    <td>57.52<br>(+0.17%↑)</span></td>
    <td>38.66</td>
    <td>46.24<br>(+0.06%↑)</span></td>
    <td>49.58<br>(+0.16%↑)</span></td>
    <td>28.86<br>(-0.03%↓)</span></td>
    <td>36.48<br>(+0.03%↑)</span></td>
    <td>41.09<br>(+0.07%↑)</span></td>
  </tr>
</table>

## Conclusion
This project demonstrates that modifying nominal adjectives (JJ) to nouns (NN) in POS tags leads to a slight increase in precision and F1 score for coreference resolution, despite a minimal impact on recall. The results suggest that such adjustments can improve the linguistic accuracy and effectiveness of coreference systems.

## Dependencies and Installation
- Python version: 3.x
- Stanford NLP version: 4.5.6
- CoNll 2011 scorer version: v8.01

## Acknowledgments
Thanks to Sameer Pradhan for his help with data availability on the CoNLL 2011 website.
