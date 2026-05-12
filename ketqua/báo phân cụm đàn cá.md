Kaur et al. J Wireless Com Network (2024) 2024:92 EURASIP Journal on Wireless
https://doi.org/10.1186/s13638‑024‑02422‑z
Communications and Networking
RESEARCH Open Access
Energy‑efficient artificial fish swarm‑based
clustering protocol for enhancing network
lifetime in underwater wireless sensor networks
Puneet Kaur1, Kiranbir Kaur1, Kuldeep Singh2, Kiran Saleem3, Ateeq Ur Rehman4*, Rupesh Gupta5 and
Seada Hussen Adem6*
*Correspondence:
Abstract
202411144@gachon.ac.kr; seada.
hussen@aastu.edu.et Underwater wireless sensor networks (UWSNs) face significant challenges, such as lim-
1 Department of Computer ited energy resources, high propagation delays, and harsh underwater environments.
Engineering & Technology, Efficient clustering can help address these challenges by grouping nearby nodes
Guru Nanak Dev University,
to minimize network fragmentation and balance energy consumption. However,
Amritsar 143005, India
2 Department of Electronics placing gateways near the sink node can result in increased communication overhead
Technology, Guru Nanak Dev and higher energy consumption in regions with concentrated data flow. To address
University, Amritsar 143005, India
these issues, we propose an energy-efficient artificial fish swarm-based clustering
3 School of Software, Dalian
University of Technology, Dalian, cognitive intelligence protocol (EAFSCCIP). EAFSCCIP leverages the collective behavior
China of artificial fish within a Bees algorithm framework, using a combination of heuristic
4 School of Computing, Gachon
and metaheuristic approaches for optimal cluster-head (CH) selection in each round.
University, Seongnam-si 13120,
Republic of Korea The protocol focuses on reducing energy consumption and extending network life-
5 Chitkara University Institute time by considering real-time energy levels and the proximity of nodes for CH selec-
of Engineering and Technology,
tion. Simulations have been executed in NS3 to validate and compare the performance
Chitkara University, Rajpura,
Punjab, India of the proposed algorithm with the existing clustering protocols. The results indicate
6 Department of Electrical Power, that EAFSCCIP significantly enhances the packet delivery ratio (PDR) by an average
Adama Science and Technology
of 5.33% over existing methods and improves network lifetime by 6.54% compared
University, 1888 Adama, Ethiopia
to traditional protocols. It also reduces energy consumption by 25.6% and decreases
packet loss by 50.5%, while achieving 20.4% higher throughput at the initial stage.
These improvements make EAFSCCIP a promising solution for applications like acoustic
monitoring in UWSNs, providing a balance between energy efficiency and reliable data
transmission.
Keywords: Underwater wireless sensor network (UWSN), Acoustic monitoring, Energy
efficiency, Clustering, Artificial fish swarm algorithm (AFSA)
1 Introduction
The increasing demand for real-time data collection, remote monitoring and auton-
omous operation in underwater environment has motivated the development of
underwater wireless sensor networks (UWSNs) [1]. Conventional electromagnetic
radio waves are ineffective for underwater applications due to the difficulties imposed
by seawater. Therefore, acoustic waves have been established as the best medium due
© The Author(s) 2024. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long
as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you
modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of
it. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise
in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted
by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy
of this licence, visit http:// creat iveco mmons. org/ licen ses/ by- nc- nd/4. 0/.

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 2 of 27
to their outstanding results when opening underwater communication [2]. UWSNs
represent intricate, self-organizing networks comprising acoustic sensor nodes that
operate beneath the water’s surface [3]. With the growing human underwater activi-
ties, more application scenarios are emerging for the UWSNs. These applications
across various domains such as navigation assistance, disaster prevention (through
earthquake and tsunami warnings), environmental monitoring (covering sea cur-
rents, wind patterns, and fish tracking), exploratory missions (encompassing oil, min-
eral, and fish detection), and tactical surveillance [4]. Over the past years, there have
been significant strides in the progress of routing algorithms designed for terrestrial
WSNs [5–10]. However, routing systems have distinct obstacles while maneuvering in
underwater environments due to the aquatic conditions. The constraints comprehend
limited data transmission speeds, lack of channel capacity, notable signal weakening,
considerable delays, heightened bit error rates, augmented energy consumption, and
dynamic changes in network structure. Hence, conventional routing protocols are not
appropriate for direct implementation in UWSNs. Acoustic transmissions in UWSNs
have much lower energy levels equated to radio signals. This results in longer delays
and raised error rates for data packets that are transferred. To effectively tackle the
distinct challenges posed by underwater environments, it becomes imperative to
develop underwater-specific routing protocols to ensure energy-efficient communica-
tion while meeting the unique performance requirements demanded by UWSNs [11].
While numerous routing strategies have been developed to alleviate the strain on
energy resources in UWSNs, the persistent hotspot problem continues to challenge
these networks, leading to premature sensor failure. To address this issue [12–14],
clustering approaches stand out as a superior solution. Cluster-based routing proto-
cols are designed to optimize network performance by organizing sensor nodes into
clusters. In this arrangement, each cluster is typically managed by a cluster head (CH)
tasked with the aggregation and transmission of data to a base station (i.e., sink) [13].
Using the process of data aggregation, clustering technology reduces the volume of
packets traversing the network, channeling data through CHs [15]. The decrease in
both the quantity of active nodes and the collective energy consumption among these
nodes plays a vital role in extending the overall lifespan of the network [16]. To over-
come the aforementioned challenges and bridge the existing gaps in research, we pre-
sent an energy-efficient artificial fish swarm-based clustering cognitive intelligence
protocol (EAFSCCIP). This protocol is specifically designed for acoustic monitoring
within UWSNs, addressing critical issues and advancing the field. Our contribution
in introducing the EAFSCCIP protocol holds significant importance for the following
reasons:
• The proposed EAFSCCIP protocol addresses the unique challenges of UWSNs
stemming from the dynamic nature of the underwater environment, limited com-
munication ranges, and high energy demands.
• To the best of our knowledge, EAFSCCIP is the first ensemble heuristic-
metaheuristic clustering protocol for UWSNs, which simultaneously benefits
from the advantages of heuristics (fast-speed knowledge-aware) and metaheuris-
tics (high performance).

K aur et al. J Wireless Com Network (2024) 2024:92 Page 3 of 27
• Presenting a metaheuristic-driven clustering protocol rooted in the artificial fish
swarm algorithm (AFSA) to attain a proper distribution of CHs, ensuring balanced
coverage while minimizing the network’s energy consumption.
• Employing a heuristic knowledge-based algorithm utilizing the local fitness values of
the sensor nodes to guide the search process of the AFSA.
• Providing comprehensive simulations to assess the performance of EAFSCCIP
against state-of-the-art heuristic and metaheuristic techniques in terms of network
lifetime, energy efficiency, packet loss, data delivery, and throughput.
The structure of this paper is as follows: In Sect. 2, we embark on an exhaustive explora-
tion of the current routing protocols employed in UWSNs. Section 3 provides a thor-
ough exposition of the proposed EAFSCCIP. Moving to Sect. 4, we present the outcomes
derived from our experiments, encompassing an in-depth analysis of the results along-
side comparisons with established methodologies. Finally, in Sect. 5, we provide our
conclusions by and delineating prospective avenues for future research endeavors.
2 Related work
Typically, UWSNs are intentionally self-organizing and self-healing, with sensors
intercommunicating with each other to optimize data collection and transmission.
Ongoing research and development efforts are focused on improving the capabilities
of UWSNs, including increased communication range, improved energy efficiency,
and higher data transmission rates. These meliorations will further enhance the
potential for underwater wireless sensors to overturn underwater data collection
and monitoring. Acoustic UWSNs comprise underwater environments where col-
laborative monitoring tasks are undertaken through the deployment of acoustic sen-
sor nodes and underwater unmanned submarine vehicles, specifically tailored for
such aquatic settings [2, 3, 16]. Many routing strategies have been developed to
lessen the load on UWSNs’ energy resources and increase their operational lifetime
[13]. For dealing with a small-scale UWSN, the scheduling technique may be used
effectively; however, due to the significant latency in acoustic connections, this
approach is not viable when dealing with a large-scale UWSN [17]. Because of this,
clustering techniques have been developed, whereby the nodes closest to the clus-
ter’s center form subgroups [15], and the other nodes eventually merge into these
larger groups. In the following, the existing clustering techniques used for UWSNs
are reviewed. In the original LEACH method [18], the choice of CHs relies solely on
a predetermined threshold function, without considering other factors affecting net-
work longevity. To address this issue, I-LEACH [19] introduced enhancements by
selecting CHs based on residual energy, node location, and neighboring node counts.
Meanwhile, LEACH-C [20] offers a centralized LEACH-based approach that opti-
mizes CH selection considering the remaining energy of nodes. LEACH-C addresses
the inefficiencies of traditional LEACH by selecting the most qualified CHs from a
pool of candidates. During the initial stage, nodes communicate their locations and
remaining energy to the sink, enabling the sink to choose CHs with higher energy
reserves. This arrangement helps to optimize the network, with all other nodes
working as traditional sensors (similarly to what happens in LEACH). Cluster-based

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 4 of 27
ant colony optimization network (CACONET) [21] evaluates the performance of a
cluster and CHs by evaluating average size cluster contract length. The system
arranges the sensor nodes to well-formed groups such that strong and cost-effective
link connectivity can be guaranteed for each group. For this purpose, many traits
like network grid sizes and over all node numbers in addition to the initial transmis-
sion flows of nodes have been picked out for your examine too with regards to meas-
ure comprehensively the efficacy of CACONET. CACONET has been designed to
maximize clustering benefits by considering many parameters like node transmis-
sion range, directionality and mobility of a typical ad hoc MANET. The Distributed
Underwater Clustering Method (DUCS) [22] is an example of the clustering method
in UWSNs. The system relies on a decentralized architecture to create clusters,
allowing the nodes to self-organize into several layers of cluster hierarchies. Energy-
efficient and balanced energy consumption cluster-head routing protocol (EBECRP)
[17] uses clustering technology to diminish the necessity of multi-hop selection and
decrease energy consumption. Mobile sinks are used to distribute the workload
evenly among nodes, while clustering is applied to reduce both the number of multi-
hop choices and the amount of energy used. Cluster-based energy-efficient routing
(CBE2R) [23] is a method that minimizes energy use while maximizing productivity.
According to this paradigm, the ocean may be conceptualized as consisting of seven
distinct strata. These layers have contained additional nodes that gradually improve
the battery life of the nodes as they condescend from the top. The sensor nodes
transmit the conglomerated information to the hub through the transport nodes,
also known as CHs, which typically possess more energy and memory capacities.
Courier nodes establish a cluster by engaging in communication with their immedi-
ate environment through the transmission of a ”join” message. Cluster-based multi-
path shortest-distance energy-efficient routing (CMSE2R) [24] introduces a method
dwelling of four stages for clustering in UWSNs. The steps encompass network con-
figuration, cluster creation, intra-cluster connectivity, and data sharing. It demon-
strates several connections within the same cluster and optimizes the exchange of
data. The protocol significantly meliorates the quality of connections by using sta-
tionary carrier nodes and performing multi-path routing, making it an economical
alternative for transmitting data with little energy consumption in UWSNs. ACUN
[25] selects CHs according to the remaining energy of nodes and loss in energy along
the path. The method uses a multi-level adaptive clustering mechanism to efficiently
deploy sensor nodes. The cluster formation is dynamically reconfigured according to
the energy levels of the network. ACUN enhances the energy efficiency of the net-
work and prolongs its lifetime by controlling CHs and data paths. Yet the available
study does not account for distance. Cluster-based underwater wireless sensor net-
work (CUWSN) [26] is based on the selection of CHs, which are chosen by taking
into account a remainder energy level of nodes and multi-hop routing for transmit-
ting data packets to the targeted node. Based on extensive simulations and investiga-
tions, the research presents important guidelines in choosing protocols for managing
energy efficiency as well network lifetime optimization under underwater contexts.
Even if the CUWSN can improve networking performance and energy consumption,
but its advantages are not reflected in long range and multi-hop scenarios. Junfeng

K aur et al. J Wireless Com Network (2024) 2024:92 Page 5 of 27
et al. proposed the AMDC routing protocol, which is mainly designed for mote plat-
forms [16]. [27], which was specifically designed for UWSNs due to the severe fad-
ing channel effects in underwater acoustic applications. The asymmetry of
underwater noise, and the reduced intensity of the signal in a low-SNR regime typi-
cal for most underwater propagation contexts are taken into account by this proto-
col. The method focuses on a multi-path partition approach that divides the
transmission line to sink node into multiple links with different qualities. Looking to
see whether it would be practical, the researchers researched the benefits of using
irregular paths to make data transmission more reliable and as efficient as possible.
Coutinho et al. [28] proposed GEDAR system which exploited the concepts spatial
routing with opportunistic routing algorithms to improve data delivery in UWSN.
Position-based opportunistic data dissemination helped to accommodate the con-
straints of underwater routing, such as large attenuation and topology variation.
This protocol increases energy efficiency of the network by moving away from tradi-
tional approach where control messages are used to discover and keep routes alive
through idle areas. The above protocol instead has implemented a recovery mode
through topology control by playing with the depth of such void nodes. As we men-
tioned before, the limited energy and an inconvenient power replacement in under-
water sensor networks also will lead a network to be destroyed quickly even with
one single faulty node. This paper presents an adaptive cluster-based routing proto-
col using MARL method which helps nodes to jointly choose the most optimal
routes. An adaptive cluster-head selection saves energy, reduces hotspots, and does
not require the additional communication overhead or convergence criteria from
neighboring nodes for automatic routing decisions based on local information. The
biased reward function also leads to routes favoring the channel over cluster heads,
since using a CH is beneficial in such aspects [29]. In underwater sensor network,
owing to the energy constraints and difficulty for power replacement as well as lim-
ited mobility of nodes at sea, a single malicious node can significantly shorten the
lifetime of such networks through this kind attack. This paper presents an adaptive
clustering routing protocol using multi-agent reinforcement learning in which nodes
take advantage of other and get the best route from source to destination. A cluster-
head selection algorithm, which adapts itself to the routing and environmental data
is postulated in order to mitigate hotspots without additional communication over-
head or consensus from neighboring nodes but allows self-decision making (relied
upon information uplinked). A reward function that is biased in this respect helps us
to further bias routing toward using cluster heads as relays [30]. Quality of service
evolutionary routing protocol (QERP) [31] is another cluster-based protocol that
focuses on optimizing data transmission in UWSNs while ensuring Quality of Ser-
vice (QoS). It incorporates an evolutionary algorithm to adapt to the unique chal-
lenges of underwater environments, such as variable link quality and energy
constraints. This protocol enhances the rate of successful packet delivery, reduces
the average end-to-end delay, mitigates energy consumption, and fulfills QoS crite-
ria. Our review of the literature revealed that researchers have employed diverse
clustering protocols in terrestrial WSNs, while relatively fewer techniques have been
explored for UWSNs. A comprehensive comparison of the reviewed techniques is

```
Table 1 | Qualitative comparison of the existing clustering techniques
| Protocol   | Energy efficiency | Scalability | Fault tolerance | Reliability | Network longevity | Delays | Clustering overhead | Load balancing |
|------------|-------------------|-------------|-----------------|-------------|-------------------|--------|---------------------|----------------|
| LEACH [18] | +                 | 0           | –               | +           | –                 | +      | +                   | 0              |
| H-LEACH [19]| +                | 0           | +               | +           | 0                 | +      | +                   | +              |
| LEACH-C [20]| –                | +           | –               | +           | –                 | +      | 0                   | +              |
| CACONET [21]| 0                | +           | –               | 0           | +                 | –      | +                   | 0              |
| EBEC(R) [17]| 0                | 0           | –               | –           | +                 | +      | +                   | +              |
| CBE2R [23]  | –                | +           | 0               | –           | –                 | 0      | 0                   | –              |
| CMSE2R [24] | +                | –           | +               | 0           | 0                 | +      | +                   | +              |
| ACUN [25]   | 0                | 0           | +               | –           | –                 | –      | –                   | –              |
| CLWSN [26]  | +                | –           | –               | +           | –                 | 0      | 0                   | –              |
| AMDC [27]   | –                | –           | 0               | +           | –                 | –      | –                   | 0              |
| GEDAR [28]  | +                | 0           | +               | +           | –                 | +      | 0                   | 0              |
| QERP [31]   | 0                | +           | –               | –           | –                 | –      | +                   | –              |

Table 2 | Advantages and deficiencies of the existing clustering techniques
| Protocol   | Advantages                                                                                   | Deficiencies                                                                                 |
|------------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| LEACH [18] | Reducing energy consumption—Can handle a large number of nodes—Distributing CH selection    | Unequal clustering—Limited data aggregation                                                  |
| H-LEACH [19]| Reducing energy consumption—Probabilistic algorithm                                         | Limited scalability—Limited load balancing                                                    |
| LEACH-C [20]| Deterministic algorithm to select CHs—Reducing energy consumption—Balancing the workload    | Limited scalability—Complex algorithm                                                         |
| CACONET [21]| Robust communication—Packet routing cost is minimized                                       | Number of nodes are not dynamic—Complex system                                                |
| EBEC(R) [17]| Avoiding depth base routing—Good balance of load—Reducing communication overhead           | Number of transmissions—Lifetime is not independent                                           |
| CBE2R [23] | Low energy consumption—Considering propagation delay—Transmission loss is reduced           | All is dependent on setup phase—Re-clustering                                                  |
| CMSE2R [24]| Improving the link quality—Reducing the average energy consumption                          | Multi-path route development is complex                                                        |
| ACUN [25]  | Using a multi-level hierarchical network—Excessive energy burdens reduced—Energy balance    | No fault tolerance mechanism                                                                  |
| CLWSN [26] | High average path loss—High throughput                                                      | Fixed and short communication scale—Area coverage Security                                    |
| AMDC [27]  | High energy efficiency—Better total Packet Error Rate (PER)                                 | Complexity and difficulty to scale directly                                                   |
| GEDAR [28] | Improving the network performance—Balancing network traffic loads                           | Topology dependable—Lifetime of the network is dependable                                     |
| QERP [31]  | Low energy consumption—High packet delivery ratio—Low network delay                         | High network traffic and node density—High the probability of collisions                      |
```

K aur et al. J Wireless Com Network (2024) 2024:92 Page 7 of 27
varying energy levels), scalability to large-scale UWSNs, and cross-layer
optimization.
3 Proposed methodology
In this section, we will delve into the network model, energy model, clustering
model, and data transmission scheme. These processes are discussed in the following
subsections.
3.1 Network model and communication integration in the EAFSCCIP protocol
The network model used in the EAFSCCIP protocol, illustrated in Fig. 1, is a three-
dimensional (3D) UWSN designed to enhance the selection of CH nodes during each
data transmission round. This model aims to optimize network performance by bal-
ancing energy consumption, improving data delivery efficiency, and extending network
lifetime through intelligent clustering and communication strategies. The model consid-
ers both the spatial distribution of sensor nodes and the dynamic nature of underwater
environments.
The communication protocol plays a central role in the EAFSCCIP framework, facili-
tating the selection of the most suitable forwarding node for data transmission based
on real-time situational information such as residual energy, node position, and signal
strength. The protocol employs a knowledge-based heuristic-metaheuristic approach,
where the decision-making process is informed by local node information and global
network state, ensuring the efficient selection of CHs to minimize energy consumption
and maximize network coverage.
In the UWSN setup, a stationary sink node is deployed at the ground level, acting as
a central data collection point. The sink node is equipped with Radio Frequency (RF)
transceivers to enable communication with surface-level monitoring systems, allowing it
to interface with terrestrial infrastructure or satellite links. The sink acts as the primary
interface between the underwater sensor network and external systems, enabling data
retrieval and network management.
Fig. 1 Network model of the proposed EAFSCCIP protocol

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 8 of 27
Mobile sensor nodes are deployed across the seabed, capable of sensing environmen-
tal parameters such as temperature, salinity, and pressure. These nodes are equipped
with acoustic modems, which enable them to communicate with each other and the sink
using underwater acoustic signals. Acoustic communication is chosen due to its superior
range compared to electromagnetic waves in water, as sound waves can propagate over
longer distances with lower attenuation in an aquatic environment. This makes acoustic
signals the preferred medium for data exchange in UWSNs.
The communication process within the EAFSCCIP protocol involves multiple stages:
• Cluster Formation The network is divided into clusters, with each cluster consisting
of a CH and multiple member nodes. The CH is responsible for aggregating data
from its member nodes and transmitting the combined data to the sink node. This
clustering strategy reduces the communication burden on individual nodes and helps
in conserving energy.
• Cluster-Head Selection The CH selection is based on a combination of factors includ-
ing the residual energy of nodes, their proximity to other nodes, and their ability to
maintain reliable communication links. This decision is dynamic and adaptive, allow-
ing for the rotation of CH roles among nodes to evenly distribute the energy load and
avoid the rapid depletion of any single node’s battery.
• Data Transmission Once a CH is selected, it gathers data from its member nodes
through acoustic communication links. The data is aggregated to reduce redundancy
and then transmitted to the sink node using multi-hop communication if necessary.
• Energy Management Throughout this process, the protocol carefully manages energy
consumption by adjusting transmission power based on the distance between nodes,
ensuring minimal energy wastage while maintaining strong communication links.
3.2 Bidirectional communication and collaboration
In the model formulated here, all of these nodes have two-way communications capa-
bility with each other providing a means for an interconnected alliance between the
entities. This intertwines more closely with the notion of communication, as nodes are
communicating their observations and using this new information to jointly make deci-
sions. For example, the equation giving ”ask” and ”tell”, communication primitives would
be:
BiC=βj ask(j,i,φ)∨βitell(i,j,φ)
(1)
where βj and βi represent the knowledge bases of nodes j and i , respectively, and φ
denotes the specific context or information being shared. This exchange of information
is crucial for determining the CH node, as nodes can ”ask” for information from other
nodes or ”inform” them of their status, thereby influencing CH selection.
3.3 Cluster‑based organization with enhanced communication
This cluster-based network model groups sensor nodes into a series of clusters, each
managed by a CH whose role is to act as the local coordinator on behalf all its mem-
bers. The CH selection process in view of the same communication model determines

K aur et al. J Wireless Com Network (2024) 2024:92 Page 9 of 27
acceptable nodes for serving as a CH based on what it knows from three perspectives:
information, energy and connectivity. By defining an appropriateness Si for each node,
we can mathematically model the CH selection as:
S =w ·E +w ·C +w ·κ
i 1 i 2 i 3 i (2)
where E i is the energy level of node i, C i is the connectivity score of node i with other
nodes, K i is the knowledge base factor reflecting the situational awareness of node i, and
w 1 , w 2 , and w 3 are weighting factors that balance these attributes.
This equation helps in selecting the CH by considering not just energy and connectiv-
ity but also the node’s situational awareness, which is enhanced through the communi-
cation model.
3.4 Assumptions and communication dynamics
It is also expected that the assumptions on which EAFSCCIP protocol was built, include
homogeneous initial level of batteries in nodes and only equipped with GPS will directly
facilitate communication model. For example, the GPS enabled nodes can send their
locations to other neighboring data which will help in routing of maximum informa-
tion. Further, the nodes are stationary during this simulation period and hence easier for
communication. The reliability of communication paths is critical, and we can model the
communication reliability R ij between nodes i and j as:
1
R = ·exp(−γ ·L )
ij 1+dα ij (3)
ij
where d ij is the distance between nodes i and j, α is the path-loss exponent, L ij represents
γ
the interference level between nodes, and is a constant reflecting the sensitivity of the
communication link to interference.
This equation ensures that nodes prioritize communication paths with higher reliabil-
ity, directly impacting CH selection and routing decisions.
3.5 Dynamic decision making in communication
The proposed system, with n agents acting as intelligent nodes, is dynamic and adaptive.
Each node i continuously updates its knowledge base
KBi
through communication with
other nodes. The knowledge base is updated using:
KBi(t+1)=KBi(t)∪{φ
j→i
:φ ∈KBj}
(4)
φ
where j→i represents the information transmitted from node j to node i at time t. This
updated knowledge is then used to make informed decisions about CH selection, power
adjustments, or rerouting to avoid interference. For example, if a node receives new situ-
ational data φ , it may adjust its CH suitability score S i as:
S(t+1)=S(t)+δ·ψ(φ)
i i (5)
δ ψ(φ)
where is an adjustment factor and is a function that quantifies the impact of the
ψ
new information on the node’s suitability.

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 10 of 27
3.6 Updated energy model for UWSNs in the EAFSCCIP protocol
Modeling of energy in UWSNs, especially focusing on the EAFSCCIP protocol to dem-
onstrate its working, is very important to know how much energy will be utilized while
transmitting and receiving data. Another unconventional scenario is the underwater
where there are special issues, notably a higher signal attenuation and energy demands
due to being an aquatic medium. As access to energy can be a bottleneck, especially
when power supplies are limited and non-rechargeable, the importance of being aware
and designing according to an accurate model is crucial for optimal network perfor-
mance as well as prolonging battery lifetime.
3.7 Transmission and reception energy consumption
The energy consumption for transmitting a data packet from one node to another (or to
a sink node) is influenced by various factors, including the distance between nodes, the
modulation techniques employed, and the depth of the underwater environment. The
energy required for E tx transmission is given by:
E =l·(E +E ·dµ)
tx elc amp (6)
where l is the length of the data packet (in bits), d is the distance between the transmit-
ting and receiving nodes (in meters), E elec is the energy required for the electronics of
the transmitter, E amp is the energy used by the amplifier to transmit the signal, and µ is
the path-loss exponent.
For reception, the energy consumption E rx is primarily associated with the electronic
components required to decode the incoming signal and analyze the received data:
E =l·E
rx elc (7)
These equations emphasize that both transmission and reception are energy-intensive
processes, particularly in the challenging underwater environment.
3.8 Total energy consumption of a CH node
Given that the EAFSCCIP protocol organizes sensor nodes into clusters, the energy
consumption of a CH node becomes a critical factor in the overall network efficiency.
The total energy consumption E CH of a CH node in a single round of data transmission
(assuming no data aggregation) can be expressed as:
E =n·E +(n+1)·E
CH rx tx (8)
where:
• n is the number of member nodes in the cluster,
• E rx and E tx are as defined above.
Additionally, the distance between the CH node and the sink node D plays a significant
role in determining the transmission energy. The total energy consumed by the CH for
communication with the sink is:

K aur et al. J Wireless Com Network (2024) 2024:92 Page 11 of 27
E =(n+1)·l·(E +E ·Dµ)
CH_sink elc amp (9)
3.9 Energy‑aware communication and mobility considerations
To maintain cluster stability and minimize excessive energy consumption due to
frequent CH re-election or interface refreshing, the EAFSCCIP protocol integrates
mobility data to establish more stable connections among nodes with less frequent
movement. This approach reduces the control overhead and extends the network’s
operational lifetime.
Energy consumption over a time interval
(cid:31)t
can be calculated based on the change
in residual energy during this period:
E =E (t)−E (t+�t)
CONS RES RES (10)
where E CONS is the energy consumption between the start time t and the end time
and E RES (t) and E RES (t+�t) are the residual energy levels at times i and (t+�t),
respectively.
This equation allows for continuous monitoring of energy depletion, which can
inform dynamic adjustments in the communication and network models, such as
rerouting decisions or CH re-selection, based on current energy levels and node
connectivity.
3.10 Path selection based on energy efficiency
In alignment with the communication model’s decision-making process, the protocol
employs a max-min routing strategy to select paths with the highest remaining energy
in bottleneck nodes. Alternatively, the maximum efficiency routing strategy selects
paths with the lowest overall energy consumption for packet transmission.
The energy efficiency E of a path can be modeled as:
eff
1
E =
eff m E (11)
i=1 CONSi
(cid:31)
where m is the number of nodes on the path and E CONSi is the energy consumption of
the i-th node on the path.
As shown in above discussion, this energy model along with the communication
and network models help to ensure that the EAFSCCIP protocol not only serves as
an energy conserving solution but it also responds dynamically to changes occurring
within UWSN environment which helps in achieving a more dependable and effective
overall operation of network.
In order to update the description of AFSA-based clustering algorithm for cluster-
head selection in UWSNs by embedding belief-desire-intention (BDI) method, and
present its content from this point-of-view, environment in which decision making
would be based on ever-changing conditions, or more importantly a hostile environ-
ment that does not care about probabilities (beliefs) to begin with it is evident the
BDI model would fit perfectly.

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 12 of 27
3.11 Solution representation
This section describes how to represent a CH (artificial fish) as a feasible solution for
selection by AFSA algorithm using BDI model. The solution can be seen as a binary
string of N bits, where runtime assesses the number of alive sensor nodes. Every
sensor node is considered an agent and value associated with each bit in the string
decides decision of if Each agents own BDI framework:
Belief: The agent’s belief about the state of its environment, including the energy
levels of itself and neighboring nodes, the distance to potential CHs, and the network
topology. Desire: The agent’s goal, which is to either become a CH to optimize the
network’s energy efficiency and communication reliability or to remain a non-CH
node to conserve energy. Intention: The agent’s commitment to a plan of action, such
as electing itself as a CH or deferring to another node based on its evaluation of the
network conditions.
Where a “0” in the kth bit means that an agent would want to remain a non-CH
node and binary 1 is for state when it intends stop becoming CH-node. This represen-
tation is shown in Fig. 2, where red and green colors indicate its will for becoming a
CH or continue as non-CH.
The flowchart of the EAFSCCIP protocol illustrates the step-by-step process of
managing clustering and communication within an UWSN. The process begins with
the initialization of nodes and relevant parameters, such as node IDs, initial energy
levels, and communication ranges. Following this, clusters are formed based on the
spatial positions of the nodes. Clustering allows the network to manage groups of
nodes more efficiently, reducing the overall communication burden.
Once the clusters are formed, the protocol selects a CH for each cluster. The selec-
tion of CHs is based on two key criteria: the residual energy of the nodes and their
proximity to other nodes. This decision-making step ensures that the CH is not only
well-positioned within the cluster but also has sufficient energy reserves to handle
communication tasks. The CH then aggregates data from the member nodes in its
cluster, consolidating the information before sending it toward the sink.
The next step involves the CH transmitting the aggregated data to the sink, which
is typically situated at the surface. This transmission uses acoustic signals, which are
well-suited for underwater communication due to their ability to travel over long dis-
tances in aquatic environments.
After data transmission, the protocol evaluates whether the energy levels of the CH
have dropped below a certain threshold. If the energy is below the threshold, re-clus-
tering is triggered, meaning that new CHs are selected based on the current network
conditions. This helps in balancing the energy consumption across the network and
prolonging the overall network lifespan. If the energy levels remain above the thresh-
old, the existing CH continues its role without re-clustering. The process continues in
Fig. 2 Agents’ intentions for cluster-head (CH) selection

K aur et al. J Wireless Com Network (2024) 2024:92 Page 13 of 27
Fig. 3 Decision-making process of the EAFSCCIP protocol, highlighting adaptive CH selection to enhance
energy efficiency and extend network lifetime
a loop until the network’s operation is complete, thus ensuring efficient data collec-
tion and energy management.
Figure 3 highlights the dynamic nature of the EAFSCCIP protocol, focusing on
energy efficiency through adaptive CH selection and re-clustering, ultimately aiming
to extend the network’s lifetime while managing the unique challenges of underwater
communication.
3.12 Swarm behavior with BDI perspective
The incorporation of BDI techniques enhances the swarm behavior of the AFSA. This
approach allows agents to make more informed decisions based on their perceptions,
desires, and intentions in the environment.
3.12.1 Belief
The agent assesses its surroundings by measuring the number of adjacent nodes and
evaluating its total energy level. This information helps the agent understand its current
state and the density of nodes in its vicinity.
3.12.2 Desire
The agent seeks to move toward areas with a high concentration of resources, which is
analogous to finding better network locations. This desire drives the agent’s movement
within the swarm.

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 14 of 27
3.12.3 Intention
If the agent determines that its neighboring area has better conditions (i.e., higher
resource concentration and lower congestion), it intends to move to that location.
The agent updates its position based on the following equation:
(U −X)
X(t+1)=X(t)+STEP×RND× j i
i i ||U −X|| (12)
j i
In this equation, X i (t) represents the current position of agent i at time t , STEP denotes
the step size that determines how far the agent will move, RND is a random value that
U
introduces variability into the agent’s movement, j indicates the position of a neighbor-
(U j−X i)
ing agent or resource that the agent is aiming toward, and the term ||U j−X i|| normalizes
U
the direction of movement toward j.
3.13 Follow behavior with BDI perspective
In follow behavior, agents adopt a strategy to locate the underwater best sink target
(UBST) position within their observation area, where the concentration of resources
is highest.
3.13.1 Belief
The agent identifies the UBST with the maximum food concentration in its vicinity.
3.13.2 Intention
Agents aim for the UBST to become a cluster head, coordinating their movements
toward it.
3.13.3 Desire
If the UBST is not congested and presents a strategic advantage, the agent navigates
toward it.
The position update for the follow behavior is given by:
(U −X)
X(t+1)=X(t)+STEP×RND× BST i
i i ||U −X|| (13)
BST i
Here, X i (t) represents the current position of agent i at time t , STEP denotes the step
size that determines how far the agent will move, RND is a random value that introduces
U
variability into the agent’s movement, BST signifies the location of the identified best
sink target, and the equation structure remains consistent with the previous explanation.
3.14 Foraging behavior with BDI perspective
In foraging behavior, agents seek to enhance their positions by observing and learning
from successful strategies of neighboring nodes.

K aur et al. J Wireless Com Network (2024) 2024:92 Page 15 of 27
3.14.1 Belief
The agent collects data about the states of nearby nodes, enabling it to make informed
decisions based on the local environment.
3.14.2 Desire
The agent’s objective is to improve its position by adopting effective strategies employed
by successful neighboring agents.
3.14.3 Intention
The agent identifies a promising neighboring position U j within its detection range and
intends to move toward it. The position update for the foraging behavior is expressed
in Equation 12, and it reinforces the idea of adaptive movement based on local
observations.
3.15 Random behavior with BDI perspective
In scenarios where prior behaviors fail to yield effective results, agents resort to random
exploration.
3.15.1 Belief
The agent recognizes the absence of better options within its current state, signaling a
need for change.
3.15.2 Desire
The agent aims to prevent stagnation in local optima, which can hinder overall
performance.
3.15.3 Intention
The agent randomly selects a new position, exploring different areas of the search space
to discover potentially better solutions.
The position update in this case is given by:
X(t+1)=X(t)+STEP×RND
i i (14)
This equation reflects a simpler update mechanism, where the agent moves by a random
step size without a specific target direction, promoting exploration.
3.16 Heuristic‑empowered knowledge‑based local search with BDI perspective
In this stage, the BDI model guides the agent’s local search: Belief: The agent evaluates
its local fitness, considering factors like energy level, number of neighbors, and intra-
cluster distance. Desire: The agent aims to either become a CH or improve its cur-
rent position within the cluster. Intention: The agent selects the most promising CH
based on its local fitness and the roulette wheel selection method. This process helps

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 16 of 27
in speeding up convergence by focusing the search on promising areas of the solution
space.
3.17 Fitness evaluation with BDI perspective
The fitness function integrates the BDI model: Belief: The agent assesses the current
state of the network, including CH durability and intra-cluster distances. Desire: The
agent aims to optimize network efficiency by selecting durable CHs and minimizing
intra-cluster distances. Intention: The agent commits to a solution that best fulfills these
objectives. The fitness function is formulated as:
AvgInterDist+AvgIntraDist
Fitness=AvgEnCHs−
(cid:31) 2 (cid:30) (15)
with AvgInterDist and AvgIntraDist calculated as:
M
1
AvgInterDist= ||C −C ||
i avg (16)
M
(cid:31)i=1
N
1
AvgIntraDist= ||k−CH ||
N k (17)
(cid:31)k=1
3.18 Transmission phase with BDI perspective
In the transmission phase: Belief: CH nodes believe that aggregating data before trans-
mission will reduce redundancy and save energy. Desire: The CH nodes aim to effi-
ciently transmit data to the sink with minimal energy consumption and interference.
Intention: The nodes commit to data aggregation and secure transmission using code
division multiple access (CDMA) and Advanced Encryption Standard (AES). CDMA
ensures reliable communication by assigning unique codes to each node, reducing inter-
ference, while AES encryption secures the data transmission.
3.19 Computational complexity analysis with BDI perspective
The BDI-enhanced AFSA-driven EAFSCCIP protocol maintains a computational com-
plexity of
O(MaxIter×PopSize×CFitFun)
, where the computational complexity for
fitness evaluation
CFitFunisO(N ×M)
. This reflects the complexity involved in evalu-
ating each agent’s (sensor node’s) belief, desire, and intention across the network. Con-
sequently, the overall complexity is
O(MaxIter×PopSize×N ×M)
. This integration of
BDI techniques provides a structured framework for decision making in UWSNs, ena-
bling nodes to adapt their behavior based on dynamic environmental conditions and
network requirements.
4 Simulation setup
This section introduces the standard parametric routing protocols and the cluster-based
approach used as reference benchmarks for evaluating our proposed EAFSCCIP proto-
col. The simulation of EAFSCCIP was conducted using the NS3 simulator, specifically
utilizing the NS3 UAN (Underwater Acoustic Network) module to accurately model

K aur et al. J Wireless Com Network (2024) 2024:92 Page 17 of 27
underwater communication characteristics. The acoustic channel was configured with
a propagation speed of 1500,reflecting the typical speed of sound in water, and signal
attenuation was modeled based on frequency-dependent absorption using the Thorp
model. Additional parameters, such as ambient noise levels and multi-path effects, were
included to simulate real-world underwater acoustic conditions.
Energy consumption was modeled using the SimpleEnergyModel in NS3, where
the energy required for transmitting and receiving data packets was calculated as a func-
tion of the distance between nodes and the data packet size. Specifically, the energy con-
sumption for data transmission was modeled as:
E =l×(E +E ×d2),
tx elec amp (18)
where l is the packet size, E elec is the energy consumed by the electronics, E amp repre-
sents the amplifier energy, and d is the distance between nodes. The reception energy
was calculated as:
E =l×E .
rx elec (19)
This setup ensures a realistic assessment of energy usage in an underwater environment,
where signal attenuation and propagation delays are critical factors.
For the AFSA implementation within the simulation, we set the population size (Pop-
Size) to 50 and the maximum number of iterations (MaxIter) to 100 to ensure con-
vergence of the clustering algorithm. Additionally, the number of heuristic-empowered
solutions (HeurSize) was set to 10, allowing the protocol to use local knowledge to
refine the search for optimal cluster heads. These values were selected based on pre-
liminary testing to balance computational complexity with convergence time, ensuring
robustness in clustering and routing decisions.
× ×
The simulation environment in NS3 was configured as a 5 5 2 three-dimensional
underwater space, with sensor nodes deployed at various depths to account for depth-
related variations in pressure and signal propagation. Nodes were positioned using
a random deployment strategy, and mobility patterns were simulated using the Ran-
domWalk2dMobilityModel to represent slow node movements due to underwa-
ter currents. A stationary sink node was placed at a depth of 2 to gather data from the
sensor nodes. This setup allowed us to evaluate the EAFSCCIP protocol under realistic
underwater conditions, including variable node densities and changing environmental
parameters.
The performance of EAFSCCIP was compared against well-established clustering pro-
tocols such as LEACH, CMSE2R, and ChoA-HGS, focusing on key metrics like network
lifetime, energy consumption, and packet delivery ratio (PDR). This detailed simulation
setup ensures that the results accurately reflect the protocol’s performance in real-world
underwater scenarios.
4.1 Results
The reference protocols compared with the proposed EAFSCCIP method are LEACH
[18], CMSE2R [24], ChoA-HGS, and MOR [3]. This section consists of showing an experi-
ment that compares the operational principles from reference structure such as LEACH,

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 18 of 27
CMSE2R, ChoA-HGS and with MOR. LEACH [18] works based on the probabilistic CH
selection by the energy levels of nodes. It improves data collection and keeps power in clus-
tered networks. Related work CMSE2R [24] targets energy-efficient routing, using multi-
ple sinks and equal distribution of load across every node within a cluster to acquire the
smallest size CHs ChoA-HGS uses genetic algorithms as well adaptive honeybee mating
selection to extract on-the-fly two-hop-chosen CHs. Their objective is to extend the life
of network longer by decreasing energy consumption and increasing packet delivery rate
while determining routing decisions; MOR [3] takes multi-objective optimization consid-
erations during route selection, such that a balance between metrics including energy usage
data sending-ratio and network lifespan can be achieved. This ensures that it works con-
sistently and scales reliably to different network conditions. The challenge lies in mapping
acoustic propagation characteristics, node mobility patterns and environmental scenarios
to their counterparts for real underwater environments so as to align simulation parame-
ters with authentic under-water acoustic (UWA) channel parameters. Such alignment both
validates the correctness of simulation results and can be used in practice to guide good
protocol designs for real-world UWSNs. We evaluated these important metrics to measure
the resilience of network against Key indicators were analyzed that includes average net-
work lifetime, NED energy and drop rates, respectively [32, 33, 33–36]. The experiments
were performed in NS3 with the parameters of Table 3.
4.2 Packet delivery ratio
The PDR is a promising performance metric, and of great importance in UWSNs.
NumberofSuccessfullyDeliveredPackets
PDR= ×100%
(20)
TotalNumberofPacketsSent
Table 3 Network parameters
Parameter Value
Network size 5 km × 5 km × 2 km
Number of nodes 300, 400, 500
Sink coordinate (2000, 2000, 0)
Data packet size 1024 bits
Eelc (Energy electronics) 50 nJ/bit
Eamp (Energy amplifier) 100 pJ/bit/mµ
µ 2 5
Receiving power 50 µW
Transmission rate 1024 bps
Initial node energy 2 Joules
Acoustic channel model Rayleigh fading
Propagation speed 1500 m/s
Packet generation rate 1 packet per second
Mobility model Random waypoint
Simulation duration 1000 seconds
Node deployment Random
Battery model Linear energy drain

```
Fig. 4 PDR analysis comparison with prior approaches

Table 4 Packet delivery ratio comparison

| Density of sensor nodes | LEACH | CMSE2R | ANC   | ChoA‑HGS | MOR   | MLAR  | Proposed |
|-------------------------|-------|--------|-------|----------|-------|-------|----------|
| 100                     | 93.14 | 94.21  | 96.55 | 96.41    | 96.15 | 97.77 | 98.78    |
| 200                     | 92.10 | 93.92  | 95.73 | 95.89    | 95.50 | 96.89 | 97.13    |
| 300                     | 91.15 | 92.45  | 94.06 | 94.74    | 94.28 | 95.56 | 96.82    |
| 400                     | 90.58 | 91.13  | 93.70 | 93.41    | 93.20 | 94.90 | 96.02    |
| 500                     | 89.88 | 90.67  | 91.55 | 92.22    | 91.50 | 94.27 | 95.65    |

This graph depicts the ratio of successfully delivered packets to the total packets sent, demonstrating the reliability of the EAFSCCi2P protocol.

It indicates the rate in which we are able to transfer packets from a source node toward another, free of errors or losses. PDR analysis in UWSNs majorly contributes to understand network performance and possible issues those can degrade quality of data transmission. Results in this section we compared our EAFSCCi2P protocol with the state-of-art techniques on large scale networks in two aspects: number of nodes and simulation rounds, as shown in Fig. 4 and Table. 4 However, the performance of algorithm in every case is shown which achieves significant gains over remaining others namely EAFSCCi2P.

4.3 Network lifetime

The network lifetime in the context of UWSNs refers to how long we can keep the WSN operate on its provided resources, e.g., battery power before recharge or replacement is required. The energy consumption of each sensor itself, deployment strategy, type of communication protocols used and techniques for data processing applied influences the life span on a UWSN.
```

```
Table 5 Network lifetime comparison

| Protocol   | FND | HND | LND |
|------------|-----|-----|-----|
| LEACH      | 337 | 501 | 637 |
| CMSE2R     | 401 | 566 | 695 |
| ANC        | 411 | 625 | 701 |
| Choa-HGS   | 501 | 613 | 741 |
| MOR        | 635 | 727 | 813 |
| MLAR       | 697 | 754 | 921 |
| Proposed   | 717 | 885 | 953 |

Fig. 5 Network lifetime analysis

Network Lifetime = Total Time × (Number of Active Nodes / Total Nodes) (21)

This graph illustrates the total operational time of the network before the first node dies, reflecting the energy efficiency of the protocol compared to other methods.

In such applications, network lifetime maximization becomes the first priority as sensor nodes may be hard to access: one cannot easily go undersea just for changing or recharging sensors. In this part, we focus on analyzing the five protocols in terms of how many nodes are still alive at first node dead (FND), half nodes dead (HND) and last node dead (LND). As depicted in Fig. 5 and Table 5, it is evident that with the passage of rounds, the percentage of nodes that are still operational diminishes across all protocols. However, EAFSCCIP maintains a higher percentage of surviving nodes in comparison with the other protocols.

4.4 Energy consumption

Energy consumption holds immense significance in the context of UWSNs because these sensors are typically reliant on battery power and have constrained energy reservoirs. Consequently, the minimization of energy consumption becomes a pivotal objective, as it
```

```
Fig. 6 Energy consumption analysis

Table 6 Energy consumption comparison

| Density of sensor nodes | LEACH | CMSE2R | ANC | ChoA-HGS | MOR  | MLAR | EAFSCCIP |
|-------------------------|-------|--------|-----|----------|------|------|----------|
| 100                     | 0.2957| 0.4145 |0.4121| 0.4111   |0.4347| 0.2487| 0.2214   |
| 200                     | 0.3928| 0.4769 |0.5024| 0.4847   |0.5258| 0.3189| 0.2960   |
| 300                     | 0.5990| 0.5858 |0.5995| 0.5001   |0.6952| 0.4289| 0.3806   |
| 400                     | 0.7851| 0.7226 |0.7357| 0.6551   |0.7576| 0.5138| 0.4919   |
| 500                     | 0.9086| 0.8818 |0.8054| 0.7671   |0.8911| 0.6777| 0.6215   |

directly contributes to the extension of network lifetime while concurrently reducing the necessity for frequent maintenance and battery replacements.

\[
E_{total} = \sum_{i=1}^{N} E_i
\]

where

\[
E_i = E_{tx} + E_{rx} + E_{idle}
\]

for each node \( i \). This graph shows the cumulative energy consumption over time for different protocols, highlighting the efficiency of EAFSCCIP. In this subsection, we scrutinize the energy utilization of the different techniques in Table 6 and Fig. 6. While EAFSCCIP consumes more energy than its counterparts, it emerges as the top performer in terms of energy efficiency. Specifically, the improvements of the proposed EAFSCCIP range from 32.8% when compared to LEACH, to 24.5% versus CMSE2R, 30.2% when measured against ChoA-HGS, and 4.8% when contrasted with MOR.
```

```
Fig. 7 Packet loss rate comparison, showing how the EAFSCQIP protocol lowers packet loss rates compared to other protocols

Table 7 Comparative analysis of packet loss rates across various protocols under different network densities

| Protocols   | 100    | 200    | 300    | 400    | 500    |
|-------------|--------|--------|--------|--------|--------|
| LEACH       | 27.457 | 34.392 | 40.818 | 44.924 | 49.37  |
| CMSE2R      | 22.644 | 24.493 | 29.780 | 33.041 | 36.84  |
| ANC         | 19.554 | 22.065 | 27.299 | 28.615 | 30.57  |
| CHoA-HGS    | 17.891 | 19.746 | 22.170 | 23.374 | 24.85  |
| MOR         | 19.676 | 21.442 | 35.705 | 28.395 | 31.65  |
| MLAR        | 17.458 | 18.774 | 20.727 | 21.818 | 23.48  |
| Proposed    | 15.225 | 17.485 | 18.459 | 19.452 | 20.97  |

4.5 Packet loss

Packet loss rate pertains to the percentage of packets transmitted by sensors that fail to reach their intended destination due to various factors, including signal attenuation, noise, interference, or collisions.

```
Packet Loss Rate = \(\frac{Number\, of\, Lost\, Packets}{Total\, Packets\, Sent}\) \(\times\) 100%
```

This graph represents the percentage of packets that were lost during transmission, providing insight into the protocol's performance under various conditions.

Elevated packet loss rates can result in data inconsistencies, heightened energy consumption, and a diminished network lifespan. In Table 7 and Fig. 7, we conduct a comparative analysis of the five protocols with regard to their packet loss rates, spanning multiple rounds of simulation. Observing a linear correlation between the network load and packet loss rate in all techniques, it becomes apparent that the packet loss rate increases in tandem with heightened network demands. In contrast, our proposed algorithm consistently maintains the lowest packet loss ratio among
```

```plaintext
Fig. 8 Throughput comparison of different protocols, highlighting the superior data transmission rate of EAFSCClP across varying node densities

Table 8 Throughput performance comparison among different protocols at various sensor node densities

| Density of sensor nodes | LEACH | CMSE2R | ANC   | ChoA-HGS | MOR   | MLAR  | EAFSCCIP |
|------------------------|-------|--------|-------|----------|-------|-------|----------|
| 100                    | 0.8177| 0.7668 | 0.8978| 0.8875   | 0.9348| 0.9745| 0.9848   |
| 200                    | 0.7412| 0.7108 | 0.8611| 0.8392   | 0.9113| 0.9501| 0.9786   |
| 300                    | 0.6901| 0.6811 | 0.7957| 0.8056   | 0.8474| 0.9356| 0.9576   |
| 400                    | 0.5978| 0.6600 | 0.7221| 0.7653   | 0.8695| 0.9106| 0.9311   |
| 500                    | 0.5611| 0.6279 | 0.7011| 0.7157   | 0.8544| 0.8921| 0.9199   |

all protocols. This highlights the robustness of our algorithm in maintaining data integrity and network reliability, even under increased load conditions.

4.6 Throughput
Throughput is a vital execution metric for UWSN, addressing the quantity of data that can be transmitted effectively over a given period.

Throughput = Total Data Received / Total Time (in bits per second) (25)

This graph illustrates the rate of successful data transmission over time, indicating the efficiency of data handling in the EAFSCCIP protocol.

The obtained results in Table 8 and Fig. 8 demonstrate that the proposed EAFSCCIP seems to perform better than LEACH, CMSE2R, MOR, and ChoA-HGS techniques in grounded of throughput.
```

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 24 of 27
5 Discussion
With the EAFSCCIP’s accomplishments, it is also critical to discourse on its possible
drawbacks and areas for development. An open dialogue about issues like the protocol’s
resilience to harsh environments or susceptibility to finicky network outages helps to
create a more fair assessment and directs future research efforts. The article demon-
strates the EAFSCCIP, which is a noteworthy solution to problems in UWSNs, particu-
larly when it comes to acoustic monitoring. The improved performance of EAFSCCIP
is constantly evidenced by the comparative study conducted against recognized cluster-
ing procedures, both classical and metaheuristic-driven. Energy consumption, network
lifespan, packet delivery ratio, packet loss rate, and throughput are among the meas-
ures that depict how well the protocol works in managing the particular limitations of
UWSNs. One of the most significant features of EAFSCCIP is that it markedly extends
the network lifetime, as demonstrated by an illustrious rise in the time before the FND.
This achievement is of prime importance in UWSNs due to energy-constrained nature
and necessity for long network lifetime. The general characteristics of the EAFSCCIP
were several benefits over a broad range in network sizes as well as ability to handle vari-
able subsea environments. For a better understanding of the protocol properties as well,
a study into how it remains efficient in most scenarios with diverse node density and
transmission ranges; different communication routes will be needed. This paper deals
with one of the practical applications of EAFSCCIP useful in emergency response opera-
tion. So, though the study underscores well how it can improve network efficiency and
provide valuable emergency assistance that is necessary to establish a good use case in
real-world scenarios could be an extended examination of each individual scenario or
simulation. Though EAFSCCIP can be used for putting the ensemble knowledge-based
heuristic-metaheuristic cluster transmission protocol in real-world underwater environ-
ment, but actually there are several challenging problems that need to be solved with
great care. One major constraint is the harsh environments often found underwater.
Without the use of specialized materials and coatings to mitigate this, sensor nodes will
have a much shorter lifespan due to corrosion / rust issues. Additionally, the process
must be robust against temperature variations and changing pressure because under-
water equipment has to withstand these environmental conditions. The limitation of
energy supply is another key challenge in UWSNs. Although EAFSCCIP has an energy-
efficient design, further optimization is still necessary in order to meet the severe energy
limitation of UWSNs and prolong overall network lifetime. The propagation delays of
underwater communication are significantly greater than those operating in air, because
the speed of light/ sound is slower in water. Decision-making procedures of EAFSCCIP
should introduce strategies to respect these delays, since quick and effective cluster-
ing communication has vital importance. Not only that, but underwater environments
are much more dynamic which effect the quality of data and structuring a network.
We should develop filtering algorithms which can be used to compensate for the pres-
ence of noise in acoustic signals when implementing EAFSCCIP. While controlling the
clustering and communicating power must adapt to changes in network architecture
based on underwater dynamics. To get beyond these issues, we need tests and valida-
tion in the field. Doing real underwater experiments is difficult, because nodes must be
deployed and recovered in what are usually rocky or otherwise treacherous conditions.

K aur et al. J Wireless Com Network (2024) 2024:92 Page 25 of 27
It is essential to quantify its performance under specific conditions in order to use the
protocol practically. That calling for EAFSCCIP needs to be modulated by making it
work in different network environment s and deployability situations. Those variables
include node density, the transmission range of nodes and communication pathways on
which network efficacy—and therefore received SNR—depend. In optimization studies,
it is crucial to explore these factors so that the method works well in different scenar-
ios. Last but not least, scalability is a key factor. The EAFSCCIP should also be able to
disseminate data and composite effectively as the size of network grows. Practical scal-
ability testing is essential in order to ensure that the protocol has the ability scale with
increasing underwater sensor network sizes, as diverse marine networks shall bring an
increased level of complexity. Therefore, these issues must be tackled simultaneously for
EAFSCCIP to work successfully in real-world underwater environments, especially in
applications of acoustic monitoring when using UWSNs.
6 Conclusion
This research presents the EAFSCCIP protocol to address the inherent challenges of
UWSNs, primarily focusing on applications such as acoustic monitoring. Inspired by the
collective behavior of fish swarms, EAFSCCIP utilizes a distributed clustering algorithm
that adapts well to the unique constraints of underwater environments.
Our thorough comparative analysis with existing classical and metaheuristic-based
clustering schemes demonstrates that EAFSCCIP outperforms its counterparts in vari-
ous performance metrics, including average energy consumption over the network life-
time, PDR, packet loss rate, and throughput. In every scenario tested, EAFSCCIP has
proven effective in enhancing network performance and lifespan while promoting scal-
ability for on-demand support in emergency response situations.
Despite the valuable insights provided by EAFSCCIP for acoustic monitoring applica-
tions, certain limitations exist, particularly regarding field trials. The controlled condi-
tions of many field trials may not fully capture the randomness and complexity found in
real underwater environments. Underwater conditions exhibit unique dynamics, includ-
ing variable acoustic propagation, ambient noise fields, and water currents, which can
differ substantially from simulations in controlled settings. This discrepancy introduces
uncertainty, and thus, results from field trials should be interpreted judiciously.
7 Future work
Field trials should be designed to assess the performance of EAFSCCIP under varying
underwater conditions to determine its effectiveness in real-world applications. Practical
limitations in underwater communication, such as low bandwidth and high propagation
delays, can significantly affect the protocol’s responsiveness in real-time scenarios. It is
crucial that field trials account for these factors, especially when the protocol is expected
to deliver timely and reliable acoustic data transmission under strict QoS requirements
in diverse underwater communication environments.
Moreover, since the protocol is intended for long-term field deployments, consid-
erations regarding energy efficiency and low power consumption must be prioritized.
Although our study offers qualitative insights into the energy performance of EAFSCCIP

Kaur et al. J Wireless Com Network (2024) 2024:92 Page 26 of 27
under controlled conditions, extensive long-term field trials are necessary to evaluate
the protocol’s sustainability and optimization potential for power-efficient operation.
Our research serves as a foundation for developing effective acoustic monitoring solu-
tions in UWSNs using EAFSCCIP. However, the unpredictable nature of real-world
underwater environments highlights the need for ongoing refinement of the protocol to
ensure its robustness and adaptability in diverse and dynamic underwater settings.
Abbreviations
AES Advanced encryption standard
AFSA Artificial fish swarm algorithm
BDI Belief-desire-intention
CACONET Cluster-based ant colony optimization network
CDMA Code division multiple access
CH Cluster head
CBE2R Cluster-based energy-efficient routing
CMSE2R Cluster-based multi-path shortest-distance energy-efficient routing
CUWSN Cluster-based underwater wireless sensor network
DUCS The distributed underwater clustering method
EAFSCCIP Energy-efficient artificial fish swarm-based clustering cognitive intelligence protocol
EBECRP Energy-efficient and balanced energy consumption cluster-head routing protocol
FND First node dead
HND Half nodes dead
HeurSize Heuristic-empowered solutions
LND Last node dead
QoS Quality of service
QERP Quality of service evolutionary routing protocol
UWA Underwater acoustic
UWSNs Underwater wireless sensor networks
WSNs Wireless sensor networks
Acknowledgements
Not applicable
Author contributions
Puneet Kaur was involved in the conceptualization; data curation; formal analysis; methodology; writing—original draft;
and software. Kiranbir Kaur contributed to the investigation; methodology; writing—original draft; and writing—review
and editing. Kuldeep Singh performed the validation; investigation; and writing—review and editing. Kiran Saleem
assisted in the visualization; validation; and writing—review and editing. Ateeq Ur Rehman contributed to writing—
review and editing; methodology; and conceptualization. Rupesh Gupta was involved in the validation; investigation;
and writing—review and editing. Seada Hussen Adem was involved in the project administration; investigation; and
methodology.
Funding
No funding for this research.
Availability of data and material
Data sharing is not applicable to this article as no datasets were generated or analyzed during the current study.
Declarations
Competing Interests
All authors do not have any financial and non-financial conflict of interest.
Received: 12 September 2024 Accepted: 16 November 2024
References
1. Y. Sun, W. Ge, Y. Li, J. Yin, Cross-layer protocol based on directional reception in underwater acoustic wireless sensor
networks. J. Mar. Sci. Eng. 11(3), 666 (2023)
2. O. Alamu, T.O. OlwalK, Energy harvesting techniques for sustainable underwater wireless communication networks a
review (Energy. e-Prime Adv. Electr. Eng. Electron (2023). https:// doi. org/ 10. 1016/j. prime. 2023. 100265
3. Y. Sun, M. Zheng, X. Han, W. Ge, J. Yin, MOR: multi-objective routing for underwater acoustic wireless sensor networks.
AEU-Int. J. Electron. Commun. 158, 154444 (2023)
4. W. Guo, M. Zhu, B. Yang, Y. Wu, X. Li, Design of a self-organizing routing protocol for underwater wireless sensor networks
based on location and energy information. J. Mar. Sci. Eng. 11(8), 1620 (2023)
5. M. Shokouhifar, A. Jalali, Optimized sugeno fuzzy clustering algorithm for wireless sensor networks. Eng. Appl. Artif. Intell.
60, 16–25 (2017)

K aur et al. J Wireless Com Network (2024) 2024:92 Page 27 of 27
6. A.S. Toor, A.K. Jain, Energy aware cluster based multi-hop energy efficient routing protocol using multiple mobile nodes
(MEACBM) in wireless sensor networks. AEU-Int. J. Electron. Commun. 102, 41–53 (2019)
7. M.K. Singh, S.I. Amin, A. Choudhary, Genetic algorithm based sink mobility for energy efficient data routing in wireless
sensor networks. AEU-Int. J. Electron. Commun. 131, 153605 (2021)
8. H. Esmaeili, V. Hakami, B.M. Bidgoli, M. Shokouhifar, Application-specific clustering in wireless sensor networks using
combined fuzzy firefly algorithm and random forest. Expert Syst. Appl. 210, 118365 (2022)
9. S. A. Arif, M. H. Niaz, N. Shabbir, M. H. Zafar, S. R. Hassan and A. ur Rehman, RSSI based trilatertion for outdoor localization
in zigbee based wireless sensor networks (WSNs), In 2018 10th International Conference on Computational Intelligence
and Communication Networks (CICN), Esbjerg, Denmark, 2018, pp. 1-5
10. S. Bharany et al., ”A Review on the need of Clustering Techniques Used for Wireless Sensor Networks, In 2023 Interna-
tional Conference on Business Analytics for Technology and Security (ICBATS), Dubai, United Arab Emirates, 2023, pp. 1-7
11. S. Yadav, V. Kumar, Hybrid compressive sensing enabled energy efficient transmission of multi-hop clustered UWSNs.
AEU-Int. J. Electron. Commun. 110, 152836 (2019)
12. K.H. Syed, J. Aimin, A. Ahmad, U.R. Ateeq, A. Abbas, U.K. Wali, H. Habib, Energy efficient UAV flight path model for cluster
head selection in next-generation wireless sensor networks. Sensors 21(24), 8445 (2021)
13. S. Bharany, S. Badotra, S. Sharma, S. Rani, M. Alazab, R.H. Jhaveri, T.R. Gadekallu, Energy efficient fault tolerance techniques
in green cloud computing: a systematic survey and taxonomy. Sustain. Energy Technol. Assess. 53, 102613 (2022)
14. D. Gupta, A. Khanna, K. Shankar, V. Furtado, J.J. Rodrigues, Efficient artificial fish swarm based clustering approach on
mobility aware energy-efficient for MANET. Trans Emerging Telecommun. Technol. 30(9), e3524 (2019)
15. R. Surendran, Y. Alotaibi, A.F. Subahi, Lens-oppositional wild geese optimization based clustering scheme for wireless
sensor networks assists real time disaster management. Comput. Syst. Sci. Eng. 46(1), 835–851 (2023)
16. S. Bharany, S. Sharma, S. Badotra, O.I. Khalaf, Y. Alotaibi, S. Alghamdi, F. Alassery, Energy-efficient clustering scheme for
flying ad-hoc networks using an optimized LEACH protocol. Energies 14(19), 6016 (2021)
17. A. Majid, I. Azam, A. Waheed, M. Zain-ul-Abidin, T. Hafeez, Z.A. Khan, N. Javaid An energy efficient and balanced energy
consumption cluster based routing protocol for underwater wireless sensor networks. In 2016 IEEE 30th International
Conference on Advanced Information Networking and Applications (AINA). pp. 324-333. IEEE (2016)
18. W.R. Heinzelman, A. Chandrakasan, H. Balakrishnan. Energy-efficient communication protocol for wireless microsensor
networks. In Proceedings of the 33rd annual Hawaii international conference on system sciences p. 10. IEEE (2000)
19. Z. Beiranvand, A. Patooghy, M. Fazeli I-LEACH: An efficient routing algorithm to improve performance & to reduce
energy consumption in Wireless Sensor Networks. In The 5th Conference on Information and Knowledge Technology
pp. 13-18. IEEE (2013)
20. W.B. Heinzelman, A.P. Chandrakasan, H. Balakrishnan, An application-specific protocol architecture for wireless microsen-
sor networks. IEEE Trans. Wirel. Commun. 1(4), 660–670 (2002)
21. F. Aadil, K.B. Bajwa, S. Khan, N.M. Chaudary, A. Akram, CACONET: ant colony optimization (ACO) based clustering algo-
rithm for VANET. PLoS ONE 11(5), e0154080 (2016)
22. M.F. Khan, K.L.A. Yau, R.M. Noor, M.A. Imran, Routing schemes in FANETs: a survey. Sensors 20(1), 38 (2019)
23. M. Ahmed, M. Salleh, M.I. Channa, CBE2R: clustered-based energy efficient routing protocol for underwater wireless
sensor network. Int. J. Electron. 105(11), 1916–1930 (2018)
24. M. Ahmed, M.A. Soomro, A. Parveen, J. Akhtar, N. Naeem, CMSE2R: clustered-based multipath shortest-distance energy
efficient routing protocol for underwater wireless sensor network. Indian J. Sci. Technol 12(8), 1–7 (2019)
25. Z. Wan, S. Liu, W. Ni, Z. Xu, An energy-efficient multi-level adaptive clustering routing algorithm for underwater wireless
sensor networks. Clust. Comput. 22, 14651–14660 (2019)
26. K. Bhattacharjya, S. Alam, D. De CUWSN: energy efficient routing protocol selection for cluster based underwater wire-
less sensor network. Microsyst Technol. 28(03), 543–559 (2022). https:// doi. org/ 10. 1007/ s00542- 019- 04583-0
27. J. Xu, K. Li, G. Min, Asymmetric multi-path division communications in underwater acoustic networks with fading chan-
nels. J. Comput. Syst. Sci. 79(2), 269–278 (2013)
28. R.W. Coutinho, A. Boukerche, L.F. Vieira, A.A. Loureiro, Geographic and opportunistic routing for underwater sensor
networks. IEEE Trans. Comput. 65(2), 548–561 (2015)
29. M.F. Khan, M. Bibi, F. Aadil, J.-W. Lee, Adaptive node clustering for underwater sensor networks. Sensors 21, 4514 (2021).
https:// doi. org/ 10. 3390/ s2113 4514
30. Y. Sun, M. Zheng, X. Han, S. Li, J. Yin, Adaptive clustering routing protocol for underwater sensor networks. Ad Hoc Netw.
136, 102953 (2022)
31. M. Faheem, G. Tuna, V.C. Gungor, QERP: quality-of-service (QoS) aware evolutionary routing protocol for underwater
wireless sensor networks. IEEE Syst. J. 12(3), 2066–2073 (2017)
32. K. Saleem, L. Wang, S. Bharany, S. et al. Intelligent multi-agent model for energy-efficient communication in wireless
sensor networks. EURASIP J. on Info. Security 2024(9) (2024). https:// doi. org/ 10. 1186/ s13635- 024- 00155-6
33. S. He, Q. Li, M. Khishe, A. Salih Mohammed, H. Mohammadi, M. Mohammadi, The optimization of nodes clustering and
multi-hop routing protocol using hierarchical chimp optimization for sustainable energy efficient underwater wireless
sensor networks. Wirel. Netw. 30(1), 233–252 (2023)
34. C. Xu, S. Song, J. Liu, Y. Xu, S. Che, B. Lin, G. Xu An efficient deployment scheme with network performance modeling for
underwater wireless sensor networks. IEEE Internet Things J. 11(5), 8345–8359 (2024). https:// doi. org/ 10. 1109/ JIOT. 2023 .
33182 22
35. A. Battula, S.E. Roslin, Secure opportunistic based void-hold routing for underwater acoustic sensor networks. Opt.
Quant. Electron. 56(2), 177 (2024)
36. X. Du, Y. Zhang, Y. Wen, Z. Yang, X. Luo, J. Yan, Cluster-based fusion detection of soft and hard decisions for underwa-
ter non-cooperative targets. Signal Process. 217, 109327 (2024)
Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.