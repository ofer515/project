import gtk

class ExampleApp(gtk.Window):
    ''' An example application for pyGTK.  Instantiate
        and call the run method to run. '''
    def __init__(self):
        # Initialize window
        gtk.Window.__init__(self)
        self.set_title('pyGTK Example')
        self.set_size_request(300, 200)
        self.connect('destroy', gtk.main_quit)

        # Structure the layout vertically
        self.vbox = gtk.VBox()

        # The greeting selector --- note the use of the convenience
        # type ComboBoxText if available, otherwise convenience
        # function combo_box_new_text, which is deprecated
        if (gtk.gtk_version[1] > 24 or
            (gtk.gtk_version[1] == 24 and gtk.gtk_version[2] > 10)):
            self.greeting = gtk.ComboBoxText()
        else:
            self.greeting = gtk.combo_box_new_text()
            # fix method name to match gtk.ComboBoxText
            self.greeting.append = self.greeting.append_text

        # Add greetings
        map(self.greeting.append, ['hello', 'goodbye', 'heyo'])

        # The recipient text entry control
        self.recipient = gtk.Entry()
        self.recipient.set_text('world')

        # The go button
        self.go_button = gtk.Button('_Go')
        # Connect the go button's callback
        self.go_button.connect('clicked', self.print_out)

        # Put the controls in the vertical layout
        self.vbox.pack_start(self.greeting, False)
        self.vbox.pack_start(self.recipient, False)
        self.vbox.pack_end(self.go_button, False)

        # Add the vertical layout to the main window
        self.add(self.vbox)

    def print_out(self, *args):
        ''' Print a greeting constructed from
        the selections made by the user. '''
        print('%s, %s!' % (self.greeting.get_active_text().title(),
                           self.recipient.get_text()))
    def run(self):
        ''' Run the app. '''
        self.show_all()
        gtk.main()

app = ExampleApp()
app.run()