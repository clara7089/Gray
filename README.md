# Gray
## Inspiration
Gray's Anatomy (not the TV show, the reference book) is commonly referred to as the Bible of the medical world. Though the intersection of medicine and technology has been growing rapidly, the healthcare system is, to put it frankly, still inherently broken. Reference books are outdated, and often more time is spent than needed for basic classification problems. As a consequence, we developed Gray, a tribute to the well-reputed Gray's anatomy reference book that uses DL techniques to allow healthcare professionals to contribute to a crowd-sourced database for the general public as well as other doctors seeking a quick diagnosis. We truly believe that our project, given scale and more time, is where medicine is headed.

## What it does
Our project provides the means to explore uploaded data, classify patient samples, and upload images to fuel a growing crowd-sourced dataset.

## Ethical Considerations
### Ethical Significance
Gray provides a platform for anyone in the public to upload, classify, and explore medical image data on their own. Especially in a world without much accessibility of healthcare, Gray provides everyone with equal access to a database which they can all learn from and contribute to.

### Ethical Concerns
In providing a database of medical data for anyone to see, Gray comes with ethical concerns such as privacy and reliability of data. To address these issues, we require the data to be anonymous and plan to have a system in the future which ensures that patients consented to any images present in the database. We also worked on developing a system to authenticate users based on medical background in order to verify data classifications.

## How we built it
We utilized Flask, internal API routes, publicly available health data (mostly skin lesions from DermNetNZ), and Clarifai to power our project.

## Challenges we ran into
We ran into the problem of finding consistent and reliable image data for a variety of diseases, so we limited the scope for the purposes of simply demonstrating our site's capabilities. We also ran into numerous issues when attempting to build infrastructure around classification, but ultimately settled on a cloud-based, decentralized approach.

## Accomplishments that we're proud of
A complete product that we feel will have increasing significance within health as time goes on.

## What we learned
ML + health = power

Going into this project, most of us did not have much experience in website development. Developing Gray taught us how to create a website from scratch, use Flask to incorporate Python and communicate with the Javascript frontend, make API calls to upload and classify data, and much more.

## What's next for Gray
Authenticated users with medical licenses, higher quality data, and more disease classes. We'd also like to explore DAOs in the future, and believe we could set up a DAO for this medical application.
