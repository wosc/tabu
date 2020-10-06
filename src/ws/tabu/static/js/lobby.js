const LobbyController = {
    data: {
        'cardsets': []
    },
    init: function() {
        var self = this;
        window.fetch('./api/games', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'}
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            self.data.cardsets = data['cardsets'];
        }).catch(function(error) {
            throw error;
        });
    }
};
const CONTROLLER = LobbyController;
CONTROLLER.init();


const CardsetView = new Vue({
    el: '#cardset',
    template: '#template-cardset',
    data: {
        'context': CONTROLLER.data,
    },
});
