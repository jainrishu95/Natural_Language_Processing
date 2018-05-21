This project uses Perceptron classification algorithm to classify Hotel Reviews. 

The hotel-review is classified as True/Fake and Pos/Neg indicating whether the review is true or fake and positive or negative.
For each, a separate classification model is trained based on the training cotpus data. 

Both Vanilla Perceptron and Averaged Perceptron algorithms are used to classify the data. 
The trained model achieves the following results :

<b> Vanilla Model </b>

| Class Label |	Class Precision |	Class-Recall |	F1-Score |
| --- | --- | --- | --- |
| True	| 0.89	| 0.87	| 0.88 |
| Fake	| 0.87	| 0.89	| 0.88 |
| Pos	| 0.91	| 0.96	| 0.93 |
| Neg	| 0.95	| 0.91	| 0.93 |

Mean F1(for all four classes) : 0.9047

<b> Averaged Model </b>

| Class Label |	Class Precision |	Class-Recall |	F1-Score |
| --- | --- | --- | --- |
| True	| 0.89	| 0.86	| 0.87 |
| Fake	| 0.86	| 0.89	| 0.88 |
| Pos	| 0.92	| 0.96	| 0.94 |
| Neg	| 0.96	| 0.91	| 0.94 |

Mean F1(for all four classes) : 0.9062
