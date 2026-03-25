# Assimil scheduler

This is a basic program to schedule the sequence of lessons for the [Assimil](www.assimil.com) language learning books.

You can define multiple types of `waves` (listening, shadowing, reading, translation, etc.) to review the Assimil textbook. And this program will keep track of where you are in each wave and which lesson to review next.

## How to run
* `python3 main.py --course=SpanishAdvanced --next=5`
* `python3 -m unittest discover -s tests`

## Concepts
### Config
The config defines the review plan, the name of the log file. See the configs/ folder
### Wave
A wave is type of review.
A wave has 3 fields.
1. type
2. weights

3. filter

#### Weights
A way to manipulate the waves start date and frequency.

#### filter
