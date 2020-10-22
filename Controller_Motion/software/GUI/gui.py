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
osc = OSCThreadServer()
sock = osc.listen(address='0.0.0.0', port=8600, default=True)
cli_ip = "192.168.178.41"
cli_port = 9000

# global var
ch1_select = False
ch2_select = False
ch3_select = False
ch4_select = False


class Container(BoxLayout):
    """
    docstring
    """

    def btn1_press(self):
        global ch1_select
        ch1_select = True
        print("butten 1")

    def btn2_press(self):
        global ch2_select
        ch2_select = True
        print("butten 2")

    def btn3_press(self):
        global ch3_select
        ch3_select = True
        print("butten 3")

    def btn4_press(self):
        global ch4_select
        ch4_select = True
        print("butten 4")

    def btn1_release(self):
        global ch1_select
        ch1_select = False
        print("btn1 = False")

    def btn2_release(self):
        global ch2_select
        ch2_select = False

    def btn3_release(self):
        global ch3_select
        ch3_select = False

    def btn4_release(self):
        global ch4_select
        ch4_select = False


# Das Bewegungs anzeiger Widget
@ServerClass  # für den OSCmsg handler
class MotionDisplay(Widget):
    """
    docstring
    """
    pos_ind_ch1 = ObjectProperty(None)  # PositionIndicator
    pos_ind_ch2 = ObjectProperty(None)
    pos_ind_ch3 = ObjectProperty(None)
    pos_ind_ch4 = ObjectProperty(None)

    @osc.address_method(b'/ambiJocky/motion/ch/1/pos/xyz')
    def osc_in_ch1(self, *values):
        """
        docstring
        """
        self.pos_ind_ch1.center = self.to_parent(
            values[0]*self.width, values[1]*self.height, True)

    @osc.address_method(b'/ambiJocky/motion/ch/2/pos/xyz')
    def osc_in_ch2(self, *values):
        self.pos_ind_ch2.center = self.to_parent(
            values[0]*self.width, values[1]*self.height, True)

    @osc.address_method(b'/ambiJocky/motion/ch/3/pos/xyz')
    def osc_in_ch3(self, *values):
        self.pos_ind_ch3.center = self.to_parent(
            values[0]*self.width, values[1]*self.height, True)

    @osc.address_method(b'/ambiJocky/motion/ch/4/pos/xyz')
    def osc_in_ch4(self, *values):
        self.pos_ind_ch4.center = self.to_parent(
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

            if ch1_select:
                # den PositionIndicator auf die aktuelle Position setzte
                self.pos_ind_ch1.center = touch.pos
                # LocPos per osc senden
                osc.send_message(
                    b"/ambiJocky/motion/ch/1/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch2_select:
                self.pos_ind_ch2.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/2/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch3_select:
                self.pos_ind_ch3.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/3/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch4_select:
                self.pos_ind_ch4.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/4/pos/xyz", [x, y], cli_ip, cli_port,)

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

            if ch1_select:
                # den PositionIndicator auf die aktuelle Position setzte
                self.pos_ind_ch1.center = touch.pos
                # LocPos per osc senden
                osc.send_message(
                    b"/ambiJocky/motion/ch/1/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch2_select:
                self.pos_ind_ch2.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/2/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch3_select:
                self.pos_ind_ch3.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/3/pos/xyz", [x, y], cli_ip, cli_port,)
            if ch4_select:
                self.pos_ind_ch4.center = touch.pos
                osc.send_message(
                    b"/ambiJocky/motion/ch/4/pos/xyz", [x, y], cli_ip, cli_port,)


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
