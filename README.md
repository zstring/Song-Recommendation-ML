
## Song Recommendation based on EEG Signals using Quadratic Discriminant Analys
###Introduction
EEG Signals from Mind to detect mood and Weather based mood sensing to play the songs using Spotify API. This application was built in 24 hour hackathon - BrickHacks(MLH).

Using EEG data signals from Muse, we detect the mood of the person with 90% accuracy on training data set and 85% accuracy on test data set. We have applied Quadratic Discriminant Analysis to classify these mood signals. With this mood, using Spotify API we are able to suggest songs playlist to the user.

###Process:
- We used 4 channel data - TP9, FP1, FP2, TP10, and through each channel we used alpha and beta values. Hence, we worked with 8-D data. 
- Training data was collected using 2 subjects. Data was collected with eyes closed, and one class at a time, i.e. first happy-thoughts data was recorded, then sad-thoughts data was recorded.
- Recorded data was divided into validation and training data.
- Testing: We collected 150 simultaneous data points and passed it through the classifier. Using majority vote we decided on the class of the input sample. There was no significant delay in real-time processing.

