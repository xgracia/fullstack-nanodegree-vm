(function(){
    window.app = window.app || {};

    /* Helper Functions */
    app.helpers = {
        uuidv4: function(){
            /* https://stackoverflow.com/a/2117523 */
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
    };
})();
