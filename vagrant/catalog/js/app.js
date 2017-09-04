(function(){
    window.app = window.app || {};

    app.model = {
        data: {
            "categories": [],
            "items": []
        },
        create: function(type, name, callback){
            name = (name || '').trim();
            callback = callback || function(){};

            newData = {
                "id": app.helpers.uuidv4(),
                "name": name
            };

            // check for a valid type
            if(type === 'category'){
                types = this.data.categories;
            }
            else if(type === 'item'){
                types = this.data.items;
                newData.category = null;
            }
            else{
                // invalid type
                return;
            }

            types.push(newData);
            callback.call(this, newData);
        }
    };
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
