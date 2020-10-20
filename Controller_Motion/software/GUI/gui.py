"""
Der Erste versuch ein richtiges App für meinen Py zu schreiben


"""

# Imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from oscpy.server import OSCThreadServer
from oscpy.server import ServerClass


# Setup OSC
osc_client_ip_addr = "127.0.0.1"
osc_client_port = 9000
osc_server_port = 8000

# OSC init
osc = OSCThreadServer()
sock = osc.listen(address='0.0.0.0', port=osc_server_port, default=True)


class Container(BoxLayout):
    """
    docstring
    """

    def btn1(self):
        print("butten 1")
        osc.send_message(b'/test/button1',
                         [1], osc_client_ip_addr, osc_client_port)

    def btn2(self):
        print("butten 2")
        osc.send_message(b'/test/button2',
                         [2], osc_client_ip_addr, osc_client_port)

    def btn3(self):
        print("butten 3")
        osc.send_message(b'/test/button1',
                         [3], osc_client_ip_addr, osc_client_port)

    def btn4(self):
        print("butten 4")
        osc.send_message(b'/test/button4',
                         [4], osc_client_ip_addr, osc_client_port)


# Das Bewegungs anzeiger Widget
@ServerClass
class MotionDisplay(Widget):
    """
    docstring
    """
    pos_ind_ch1 = ObjectProperty(None)  # PositionIndicator

    @osc.address_method(b"/ambiJocky/ch1/motion/pos/cartesian")
    def callback(self, *values):
        """
        docstring
        """
        self.pos_ind_ch1.center = self.to_parent(
            values[0]*self.width, values[1]*self.height, True)

    def on_touch_down(self, touch):
        """
        docstring
        """
        # beschreäönkung auf dieses Widget
        if self.collide_point(*touch.pos):

            # in locale Widget coordinate umrechenen
            loc_pos = self.to_local(touch.x, touch.y, True)
            #print("pos: {}".format(loc_pos))

            # LocPos normalalisieren
            x = loc_pos[0] / self.width
            y = loc_pos[1] / self.height

            # den PositionIndicator auf die aktuelle Position setzte
            self.pos_ind_ch1.center = touch.pos
            # LocPos per osc senden
            osc.send_message(
                b"/ambiJocky/ch1/motion/pos/cartesian", [x, y], osc_client_ip_addr, osc_client_port)

    def on_touch_move(self, touch):
        """
        docstring
        """
        # beschreäönkung auf dieses Widget
        if self.collide_point(*touch.pos):

            # in locale Widget coordinate umrechenen
            loc_pos = self.to_local(touch.x, touch.y, True)
            #print("pos: {}".format(loc_pos))

            # LocPos normalalisieren
            x = loc_pos[0] / self.width
            y = loc_pos[1] / self.height

            # den PositionIndicator auf die aktuelle Position setzte
            self.pos_ind_ch1.center = touch.pos
            # LocPos per osc senden
            osc.send_message(
                b"/ambiJocky/ch1/motion/pos/cartesian", [x, y], osc_client_ip_addr, osc_client_port)


class PositionIndicator(Widget):
    """
    docstring
    """
    pass


# MainApp
class MainApp(App):
    """
    docsting
    """

    def build(self):
        return Container()


if __name__ == "__main__":
    MainApp().run()
