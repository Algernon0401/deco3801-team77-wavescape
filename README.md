# DECO3801 - Team "{{7*7}}"
## 042 - Friction in Design AR
    (Copied from statement of work)
    The brief we have selected is 42: Friction in Design - AR Analogue Interfaces. The brief specifies that the project is “to create an analogue interface that is mapped 100% to an AR overlay, with the overall goal of injecting friction and boundaries into AR interactions”. 

    In response to the brief, we have elected to design an interactive musical instrument and digital audio workspace (DAW) with novel analogue controls. The AR overlay will be supported by an overhead camera and projector, and the analogue interaction will be enabled primarily through the arrangement of small objects on a flat surface (e.g., a table or desk). 

    The shape or arrangement of the objects - specifically the vector (angle & distance) from a central object or point - will determine characteristics of the generated sound. The objects themselves will be specially designed (or selected), potentially with variance in shape, size and colour as means of distinction enabling further functionality. 

    This style of interface provides tangibility and an intuitive, natural method of control for the user. Additionally, a separate control board with physical controls, as well as zone features and object touch recognition will allow for advanced control of the sounds generated, and general control over the software. The combination of all these features will allow users to remain hands-free from any computer peripheral (excl. control board), whilst maintaining seamless control over the software.

    The AR overlay will enhance the experience further, by providing visual features, such as animations and flair, minimalistic GUI, boundaries and zones to separate functionality and structure DAW capabilities (e.g., recording, playback and looping).

## Folder Structure
    All project code and assets should belong in the "app" folder and all project related documents (i.e. supporting code documents, team documents) should belong in the "docs" folder.

## Style Guide
    All code written in python should adhere closely to the style guide found here: https://peps.python.org/pep-0008/   

    The bare minimum should that code is properly commented/documented, so that team members. For example,

    ```
    def do_something(self, arg1: int) -> int:
        """
            This function does something.

            Args: 
                arg1 -- An argument that alters something
            
            Returns:
                The result of doing something 
        """
    ```