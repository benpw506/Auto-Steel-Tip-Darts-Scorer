
<div align="center">
  <img src="https://github.com/user-attachments/assets/a2b2f893-a33e-46b7-a1a9-607ce83a1e82" alt="Logo height="150" width="150">
  <br/>
  <h3>Auto Steel Tip Darts Scorer</h3>
  <p align="center">An automatic scoring system for use during a game darts. </p>
  
</div>
<div>
  <h2>About the project</h2>
  <p><b>Auto Steel Tip Darts Scorer</b> is an automatic scoring solution for a game of regulation darts between two players. It is designed for use with a single webcam (tested with Logitech C920) directed at a dartboard. The program enforces the rules of a regulation darts match. These include requiring a double to checkout and win the game as well as
  reverting the players score if they bust there throw. Darts and dartboard are detecting using a YOLO v4 model created by <a href="https://github.com/wmcnally">Will McNally</a>. The model was retrained on a custom dataset of 500+ images in order to detect my personal darts and dartboard. The predictions given by the model are processed in order to track the state of the game.
</div>

<h2>Screenshots</h2>
<h3>Scoring :dart: </h3>
<div align="center">
  <br/>
<img src="https://github.com/user-attachments/assets/eafdf737-10c1-4e1e-9c46-07083b3f0795" alt="Darts detected on board" height="404" width="915" align="center">
</div>
<br/>
<h3>Checkout :trophy: </h3>
<div align="center">
  <br/>
<img src="https://github.com/user-attachments/assets/20573740-e875-4f56-90f0-725835f382c0" alt="Darts detected on board" height="404" width="915" align="center">
</div>
<br/>
<h3>Bust :x: </h3>
<div align="center">
  <br/>
<img src="https://github.com/user-attachments/assets/1eb0b081-3556-42f4-9d2a-36bc84c493f0" alt="Darts detected on board" height="404" width="915" align="center">
</div>
<br/>
<h3>Demo :video_camera:</h3>
<div>
  <h3><b>https://youtu.be/miFHaz1PGjU</b></h3>
</div>
<br/>
<h2>Getting Started</h2>
<ul>
  <li>Install conda and create a new enviroment</li>
  <li>Clone this repo  and install requirements</li>
  <li>Create a custom dataset of images</li>
  <li>Label the images using <code>annotate.py</code></li>
  <li>Crop the images using <code>crop_images.py</code></li>
  <li>Train the model using <code>train.py</code></li>
  <li>Start the scoring appliaction using <code>index.py</code></li>
</ul>

### Any questions or problems feel free to reach out :thumbsup:
















