




                           --------------------------------------------------   
                           |Server.py|  dispatching                      
                           -----------  controller (mic/moc) <-> daw communication 
                               ||
                              |  |
                             |    |
                            | osc  |    
                           |        |
                          |          |
-----------------------------raspi------------------------------------------
teensy <-> raspberry |mic.py|     |moc.py| teensy <-> raspberry 
                     --------     -------- recorder / player
                         |            |    GUI
                        |              |
                       |                |
                      |      serial      |
                     |                    |
                    |                      |
--------------------------   teensy    -------------------------------------
                |main.cpp|             |main.cpp|
