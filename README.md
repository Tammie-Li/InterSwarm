## InterSwarm: A Multimodal Semi-Physical Experimental Platform for Human-Swarm Teaming

## Abstract
Human-swarm teaming (HST) deeply integrates high-level human cognition with the distributed advantages of swarms, serving as a critical paradigm for advancing robot collectives toward real-world applications. However, existing experimental platforms are often closed, lack unified standards, and are difficult to extend. Extensive research remains confined to pure software simulations, with a severe validation gap when transitioning algorithms to physical deployment. To bridge this gap, we present a highly scalable open-source platform InterSwarm to provide a standardized integrated validation environment for decentralized swarm algorithms, human-robot interaction paradigms, and mixed-initiative teaming. InterSwarm consists of three components: (1) a scalable fleet of omnidirectional miniature robots for foundational motion control; (2) a multi-touch screen enabling occlusion-resilient localization and dynamic scene rendering; and (3) a flexible interaction framework supporting multimodal inputs and sensor fusion. Unlike conventional rigid hardware testbeds, InterSwarm emphasizes deployment flexibility and secondary development potential. It natively supports user-defined experimental protocols, allowing researchers to effortlessly integrate heterogeneous sensors and explore novel interaction modalities. Building upon pure software simulations to bridge the gap to physical reality, this modular architecture provides a low-barrier, versatile benchmark tool for physical experiments in swarm robotics, human robot interaction, and human-machine hybrid intelligence. The  project was open-sourced at https://github.com/Tammie-Li/InterSwarm. 

## Overview
![overview](/Lib/figure2.jpg "The overall architecture of the InterSwarm")
Hardware components of InterSwarm. The figure shows: (a) the overall of three components; (b) multimodal human-robot interaction system; (c-d) holonomic robot swarm; (e) dynamic environmental tracking and rendering system.

## Environmental requirements
```txt
python >= 3.6
torch >= 1.7.0
numpy >= 1.20
psychopy >= 2023.1.3
scipy >= 1.6.2
```

## Usage
### 1. One-take end-to-end demonstration of InterSwarm performing the frontier human robot interaction experiments
```python ssvep_image.py``` or ```python ssvep_stimulate.py```
 
### 2. Quantitative Analysis 
Please refer to the floder STSNN, whose data processing method is consistent with it.

### 3. One-take end-to-end demonstration of InterSwarm performing the human-swarm teaming experiments
```python main.py``` 

modified the value **paradigm_name = "semi-physics"**


### 4. One-take end-to-end demonstration of the software of InterSwarm performing the outdoor human-swarm teaming experiments
```python main.py```

modified the value **paradigm_name = "physics"**

## Disclaimer 
This project is released under the GNU General Public License (GPL). By using, modifying, or distributing this software, you agree to comply with the terms of the GPL. The authors and contributors of this project are not liable for any damages or issues arising from the use of this software. Use at your own risk. For more details, refer to the GPL license.
