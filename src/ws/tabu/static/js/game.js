const GameController = {
    data: {
        'score1': 0,
        'score2': 0,

        'card': [],
        'position': 0,
        'seed': '',

        'running': false,
        'seconds': 1,

        'card_visible': false
    },

    init: function() {
        this.connect();
    },

    connect: function() {
        const self = this;
        const loc = window.location;
        const scheme = loc.protocol === 'https:' ? 'wss://' : 'ws://';
        self.socket = new WebSocket(
            scheme + loc.host + loc.pathname + 'api/socket');
        self.socket.addEventListener('error', function(event) {
            console.log(event);
        });
        this.socket.addEventListener('message', function(event) {
            const data = JSON.parse(event.data);
            for (var key in data) {
                self.data[key] = data[key];
            }
            if (data['seconds']) {
                HourglassView.seconds = data['seconds'];
            }
        });
    },

    send: function(data) {
        this.socket.send(JSON.stringify(data));
    },

    update_score: function(variable, delta) {
        this.data[variable] += delta;
        const message = {};
        message[variable] = this.data[variable];
        this.send(message);
    },

    next_card: function() {
        this.data.position += 1;
        this.send({position: this.data.position});
    },

    toggle_hourglass: function() {
        this.data.running = !this.data.running;
        this.send({running: this.data.running});
    },

    reset_hourglass: function() {
        this.send({seconds: this.data.seconds});
    }

};
const CONTROLLER = GameController;
CONTROLLER.init();


const ScoreView = function(variable) {
    new Vue({
       el: '#' + variable,
       template: '#template-score',
       data: {
           'context': CONTROLLER.data,
           'name': variable
       },
       computed: {
           'score': function() { return this.context[variable]; }
       },
       methods: {
           decr: function(event) {
               CONTROLLER.update_score(variable, -1);
           },
           incr: function(event) {
               CONTROLLER.update_score(variable, 1);
           }
       }
    });
};

ScoreView('score1');
ScoreView('score2');


const TogglePlayer = new Vue({
    el: '#player',
    template: '#template-player',
    data: {
        'context': CONTROLLER.data,
        'title': 'Begriff anzeigen'
    },
    methods: {
        toggle: function(event) {
            this.context.card_visible = !this.context.card_visible;
            this.title = this.context.card_visible ? 'Begriff ausblenden' : 'Begriff anzeigen';
        }
    }
});


const CardView = new Vue({
    el: '#card',
    template: '#template-card',
    data: {
        'context': CONTROLLER.data
    },
    methods: {
        next: function(event) {
            CONTROLLER.next_card();
        }
    }
});


const HourglassView = new Vue({
    el: '#hourglass',
    template: '#template-hourglass',
    data: {
        'context': CONTROLLER.data,
        'seconds': CONTROLLER.data.seconds,
        'timer': null
    },
    computed: {
        'percent': function() {
            return (this.seconds / this.context.seconds) * 100;
        }
    },
    watch: {
        'context.running': function(value, previous) {
            const self = this;
            if (value) {
                if (self.timer) {
                    return;
                }
                self.timer = window.setInterval(function() {
                    self.seconds -= 1;
                    if (self.seconds <= 0) {
                        self.seconds = 0;
                        self.context.running = false;
                    }
                }, 1000);
            } else {
                if (self.timer) {
                    window.clearInterval(self.timer);
                    self.timer = null;
                }
            }
        }
    },
    methods: {
        play: function(event) {
            CONTROLLER.toggle_hourglass();
        },
        reset: function(event) {
            CONTROLLER.reset_hourglass();
            this.seconds = this.context.seconds;
        }
    }
});
