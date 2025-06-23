window.dash_clientside = window.dash_clientside || {};

window.dash_clientside.clientside = {
    enter_button: function (ns) {
        return function (n_submit) {
            if (n_submit > 0) {
                return 1;
            } else {
                return 0;
            }
        };
    },
};
