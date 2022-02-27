# Description of the Study-Cards Application

## General Structure
The application has three frames: 
* Study Sets 
* Configuration 
* Flashcards

### The Study Sets frame
This is the first frame the user encounters when the application starts running. In this frame the user can select the study set to be used from a list of available study sets. Here the user can also add new study sets to that list.

A new study set is added by importing a text file where on each row there is a term and its definition, separated by a semicolon. The term and the corresponding definition will be shown on the two sides of a single card. Once a study set is selected the user can display the Configuration frame for that study set.

### The Configuration frame
In the Configuration frame the user can define the way the study set will be presented. This includes filtering the cards in the study set to show either all the cards or just cards that have a particular tag. The tags are meant to allow the user to denote his or hers level of knowledge of the information on study card and to create groups of cards within the study set with similar level of knowledge. In this frame the user can also define the order in which the cards will be displayed, for example, in a random order, or alphabetically. Finally, the user can define which side of the cards in the study set will be shown first. In addition, this frame allows the user to see the total number of cards in the study set and the number of cards for each tag group. Note that different tags can be assigned depending on which side of the cards is shown first. A special group allows the user to view a randomly selected subset of all the cards based on the indicated level of knowledge such that cards that the user tagged as "Good" are less likely to be included in the group while cards that were tagged as "Poor" are very likely to be included in the group. 

### The Flashcards frame
In this frame the user is presented with the cards in the selected tag group, one at a time. The front side is shown first and the user can flip the card to see the back side. The user can change the knowledge tag for the card or keep is unchanged. Flipping the card can be done by clicking a button or using the *space bar* on the keyboard or by using the *down arrow* on the keyboard. Moving to the next card (or to the previous card) can also be done either by clicking a button or using the keyboard. For each card, the tagging history and the consistency level is shown to the user. A card where the tagging changes from one review session to the other will obtain a low consistency score while a card where tagging remains unchanged will obtain a high consistency score. 

## Running the Application
The code requires Python version 3.9 or higher and was tested only on a Windows 10 platform. The code in the repository includes a batch file that needs to be modified to include the relevant path. 
