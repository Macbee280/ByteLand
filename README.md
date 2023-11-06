<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->

<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/macbee280/byteland">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Enter The ByteLands</h3>

<p align="center">
    An AI-powered medieval village simulation
    <br />
    <a href="https://github.com/macbee280/byteland"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/macbee280/byteland">View Demo</a>
    ·
    <a href="https://github.com/macbee280/byteland/issues">Report Bug</a>
    ·
    <a href="https://github.com/macbee280/byteland/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<p align="center" width="100%">
    <img width="50%" src="https://github.com/Macbee280/ByteLand/blob/master/images/Picture1.jpg?raw=true">
</p>

Inspired by the joonspk-research/generative_agents project, create an AI village with multiple agents! By utilizing OpenAI, we were able to create characters that could hold conversations with each other and travel about the town.
It was created in the 2023 Gonzaga Hackathon, placed 2nd overall, and was made by 4 GU sophomores.

Features:

* Easy creation of new AI agents
* Opens a website with TTS support for the dialogue
* Infrastructure in place for a grid-based movement system for these characters

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This section below contains the major frameworks/libraries used to bootstrap our project.

* LLangChain
* OpenAI
* Django
* StreamLit
* Svelte
* gTTS

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running, you can follow these steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* streamlit
  ```sh
  streamlit run app.py
  ```

### Installation

1. Get an API Key from OpenAI [https://platform.openai.com](https://platform.openai.com)
2. Clone the repo
   ```sh
   git clone https://github.com/Macbee280/ByteLand.git
   ```
3. Create an apikey2.py file and paste the following
   ```sh
   npm install
   ```
4. Create an `apikey2.py ` file and enter the API key.
   ```py
   apikey = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Pictures:

A snapshot of the way the AI thinks and stores memory
<p align="center" width="100%">
    <img width="100%" src="https://github.com/Macbee280/ByteLand/blob/master/images/inner_thoughts.jpg?raw=true">
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [X] Add Separate AI Agents
- [X] Create pathfinding system
- [ ] Rework AI framework to have better memory systems
- [ ] Implement pathfinding and grid-based visual for users
- [ ] Demo mode and Long Term Mode
  - [ ] Specify number of days?

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Email - gdimartino@gabedimartino.com

Project Link: [https://github.com/macbee280/byteland](https://github.com/macbee280/byteland)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Contributors on this project:

* Gabe DiMartino
* Aiden Tabrah
* Izzy Tilles
* Miles Mercer

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/macbee280/byteland.svg?style=for-the-badge
[contributors-url]: https://github.com/macbee280/byteland/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/macbee280/byteland.svg?style=for-the-badge
[forks-url]: https://github.com/macbee280/byteland/network/members
[stars-shield]: https://img.shields.io/github/stars/macbee280/byteland.svg?style=for-the-badge
[stars-url]: https://github.com/macbee280/byteland/stargazers
[issues-shield]: https://img.shields.io/github/issues/macbee280/byteland.svg?style=for-the-badge
[issues-url]: https://github.com/macbee280/byteland/issues
[license-shield]:https://img.shields.io/github/license/macbee280/byteland.svg?style=for-the-badge
[license-url]: https://github.com/macbee280/byteland/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gdimartino/
[product-screenshot]: images/screenshot.png
