# Bringing AI Art to the Playa

This year I brought an interactive art experience to Burning Man. The premise was simple: you imagine an art piece, use your finger to draw a rough sketch, speak to describe the art you envision, and viola! Our magic AI turns you into a modern-day Picasso.

![](images/spongebob_circle.gif)
> Like this, but in reverse

This turned out to be a hit. We only had about 50 people check out our exhibit, but each person left with a smile and awe on their face. Given how awesome pretty much everything is at Burning Man, I’m incredibly grateful to have made even a small dent. Turns out people like having fun with AI.

It took a lot of work though! I made it a point to run the whole project 100% offline, following the Burning Man principle of Immediacy. That means I had to run my desktop computer for hours on the dusty playa. You’re probably thinking “Wow, how did you keep my computer clean!?” Oh, you don’t care? Well I’m here to tell you anyway 🌈

## Dust Proofing a Computer and Projector on the Playa

### Intro

For those who haven’t been to Burning Man: the dust is omnipresent. It gets absolutely everywhere. Furthermore, the dust is alkaline<source> and very fine (footnote: although I couldn’t find any clear data on how fine it is, only speculation online). It sticks to all things and must be washed off with soap or some acidic solution.

This presents a unique problem for electronic equipment on the Playa. The fine dust will gladly stick to any exposed circuitry, slowly corroding your equipment. And you can’t wash your circuits like your clothes.

![](images/motherboard_wash.webp)
> Don't do this pls

So obviously, you want to keep your circuits dust free. Cool story bro — put your electronics in a sealed box. Legitimately great solution.

But what if you’re crazy and you want to bring a desktop computer to the Playa to run AI algorithms on a GPU, in real time? And you want to bring the thing back home with you because you still want to play games on it later? Oh, and you want to use an expensive projector to display stuff on a screen during daytime, too. Nice.

This presents the following constraints:

- The GPU/CPU need to stay cool in a hot desert. This is a challenge because GPUs/CPUs can get quite hot during normal operation, even in the default world.
- The GPU/CPU cool themselves by dissipating their heat through a heatsink, which then gets circulated away by fans in the case. The computer needs access to cool air for circulation.
- To continue functioning beyond the Burn, all the circuits need to remain 100% dust free for the whole Burn. So there can be no dust in the circulating air.
- All of the above, now for a projector.

To solve for these, I built these glamorous dust-proof boxes:

![](images/intro_enclosures.png)

### The Build

Here, I'll go step-by-step through how I built these enclosures.

Both enclosures use roughly the same design.
- Air enters the box only through a high-quality HEPA filter, which I’ll call the ingress. All other potential holes/cracks/joints are meticulously sealed with silicone caulk or a gasket.
- Air exits the box only through designated holes, which I’ll call the egress. The egress hole(s) is smaller than the ingress hole, which ensures positive air pressure. This means that air can only flow one way (out) from the egress. We can never accidentally suck in dusty air from the egress, assuming proper operation.
- There is enough extra volume in the container for air to circulate, enabling the computer/projector heatsinks to do their job and dissipate heat away from the electronics, keeping them cool.
- The box stays closed the entire Burn. Anything that needs to be turned on/off (including the computer) uses a remote control. All cables are routed through a gasket-sealed hole that is not agitated during the Burn.


Before starting on the build, make a diagram of all input/output wires. ![wire diagram]() 

Perhaps obvious, but this helped me keep a mental model of how the whole project was going to materialize on the Playa. I only had one shot to make it work; it had to be right the first time.

#### Materials

Tools
- Dremmel for cutting/sanding holes in wood and plastic
- Power drill
- (Optional) Soldering iron to burn holes into plastic

Parts
- For computer enclosure: a large, rigid plastic storage container: https://www.homedepot.com/p/Husky-45-Gal-Latch-and-Stack-Tote-with-Wheels-in-Black-with-Red-Lid-206201/312871610 ![](images/item_husky_container.png)
  - We did not have wheels on ours
  - You want the enclosure walls to be rigid enough to hold some weight and to drill through.
  - The enclosure must be tall enough to fit the computer inside, sealed.
- For projector enclosure: A medium, clear plastic container
  - We used a restaruant food-grade container
- 3 Suction fans
  - 2 for computer, 1 for projector
- 3 PVC pipe connector tubes
  - 2 for computer, 1 for projector
- Silicone caulk
- Mounting tape
- HEPA Filters and furnace filter
- Long strips of 2-inch wide, 1-cm thick plywood
- Small thin plywood backboard
- Wood screws
- Nuts and bolts
- Garage-door sealant foam
- Duct tape


#### Computer Enclosure

1. Put computer and all electronics into the box and seal it. Make sure it all fits.

2. Cut egress holes into side wall of storage container. Insert PVC pipe connector tubes into holes.

    We used a PVC pipe connector tube as the egress. We could conveniently plug the pipe connector with a PVC plug when the computer was not in use.

    ![picture of pipe connector]() 

    1. Use the PVC tube to stencil a hole against the side of the storage container. 
    2. Use a Dremmel to cut the hole. 
    3. Sand the sides of the hole. 
    4. Insert the PVC pipe connector tube. Our pipe connector was threaded on one side, and the hole was tight enough that we could screw the connector into the container, improving the seal.
    5. Finally, seal the joint between the tube and the container with silicone caulk to prevent air leakage.

3. Cut cable hole into storage container.

    Cut a round hole somewhere near the bottom of your container. All the cables will come out of this whole, e.g. power strip cable, HDMI, USB, etc. We made this hole exactly as large as the egress, so we used a PVC pipe connector tube from the previous step to stencil the hole.

    Near the end, we will seal this hole with "gasket" made by wrapping the input/output wires in foam wrap.

4. Design and assemble an air duct out of wood that fits the HEPA filter. Attach to container.

    The suction fans need to suck air from the entire surface area of the HEPA filter for filteration to be effective. This means we can't simply put the HEPA filter flush against the suction fans; there needs to be an air duct between the fans and the filter that exposes the full surface area. I like to imagine that we're attaching a tiny slice of an A/C duct against the side of our container, only made out of wood.
    
    ![pic of john wayne]() 

    This the most challenging part of the build. Your air duct design will depend on how big your filter is and the shape of the wall of your plastic storage container. Here's how we did it:

    1. Build a wooden frame to match the height/width of your HEPA filter. The HEPA filter is attached to one side of this frame. Our frame is only 2 inches in height; in practice, this gave the duct enough volume.

    1. Test that the HEPA filter actually fits your wooden frame.

    1. To reinforce the frame (keep its square shape), we screwed it into a thin sheet of plywood board on one side. Before this though, we cut the plywood board to size so that it fit against the side of our plastic storage container.

    1. Next, you would want to attach the air duct to the side wall of the container opposite the egress. In our case, the container wall was not uniformly flat: the top 1/3 of the wall jutted out. We had to use the Dremmel to cut away a piece of the jutted-out wall such that the air duct could be attached flush to the side of the container.

    1. Use nuts/bolts to attach the air duct to the side wall of the container.

5. Cut holes through the airduct/container wall for the ingress.

    At this point, the flat plywood on the back of the airduct and the wall of the container should be flush against each other, acting as a joined surface. We want to cut holes into this joined surface for our ingress. We will mount our suction fans onto the inside of the container against these holes.

    Stencil the holes to match the size of your suction fans. Use a Dremmel to cut the holes, then sand down the sides.

8. Attach suction fans on the inside wall of the container.

    Use mounting tape to stick the suction fans against the holes you cut in the previous step. The fans should now be able to suck air through your air duct.

9.  Test the fans!

    Attach a HEPA filter to the side of your airduct somehow (we used duct tape), and plug your fans into the power. Seal the container with a lid. Check that things are working, then check for air leaks.

10. Seal any joints/holes in the air duct system with silicone caulk to prevent air leakage.
  
    Notable places we sealed:
    - **Important:** Around the suction fans, e.g. between fan and container wall
    - Joints of the square airduct brace
    - Joint between the square brace and the flat plywood board
    - Gaps between air duct frame and weird jutted-out part of the container wall

11. Stick garage sealant foam around the entire lip of container to prevent air leakage from the top.
  
    ![some picture]() The container I used would leak air under the lid when I applied positive air pressure. Sealant foam fixed this.

12. Insert computer and test the whole thing sealed.

    Ensure that air is **only** coming out of your egress holes and the wire hole.

13. When everything is ready, wrap input/output wires in foam wrap to and insert into wire hole to form a gasket.

    Test one more time. Air should now only come out of the egress holes.

14. Seal the box for the duration of the Burn!


#### Projector Enclosure

Building the projector enclosure is very similar to computer enclosure, so I'll paraphrase some of these steps.

The big notable difference is the type of plastic. The project has much harder plastic that takes longer to cut through.

1. Put the fan into the container and place the plugged-in projector on top of it. Seal the container as well as you can. Test to ensure the projector can display through the wall of the plastic container without any distortion/obstruction.

    I had to cut or burn off some plastic from the lip of my container to remove obstruction from the projector.

2. Cut egress hole into plastic container. Insert PVC pipe connector tube. Seal with silicone caulk.

    Same as computer enclosur step 2.

3. Cut cable hole into plastic container. 

    Same as computer enclosure step 3.

4. Assemble wooden air duct that fits onto bottom of container. Attach air duct to bottom of container. Add wooden legs. Cut a hole for the suction fan.

    Constructing the air duct for the projector box is somewhat similar to how we do it for the computer box, but with some notable difference.

    1. Build a rectangular wooden frame, 2 inches height, that fits onto the bottom of the plastic container. Because the projector container is much smaller, we size the frame to the container instead of to the filter. Later, we cut the HEPA filters down to fit the wooden frame.

    2. The container plastic is so rigid that we don't need a plywood back-board for maintaining the shape of the rectangular frame. Instead, we attach the frame directely to the bottom of the rigid-plastic container to form the downward air duct. We use wood screws from the inside of the plastic to attach the rectangular duct.

    3. We cut legs from a wooden fence post and attach them to the sides of the duct.

    4. Finally, we cut an ingress hole into the bottom of the plastic container into the air duct.

5. Attach suction fans against the ingress hole cut in previous step. Test the fans.

7. Seal any cracks/holes/joints with silicone caulk to prevent air leakage.

    Again, pay special attention to sealing around the suction fan!

8.  Insert projector and test the whole thing sealed.

13. When everything is ready, wrap input/output wires in foam wrap to and insert into wire hole to form a gasket.

    Test one more time. Air should now only come out of the egress holes.

14. Seal the box for the duration of the Burn!


--------------

Huge thanks to my dad, my brother, Nic Borensztein, Thomas Cheng, and Patrick Hultquist