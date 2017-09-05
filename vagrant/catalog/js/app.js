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
        },
        read: function(type, query, callback){
            query = query || {};
            // do not set a default callback, if no callback given, just return

            // check for a valid type
            if(type === 'category'){
                types = this.data.categories;
            }
            else if(type === 'item'){
                types = this.data.items;
            }
            else{
                // invalid type
                return;
            }

            // if no query was passed in...
            if(typeof(query) === 'function'){
                // set callback to that that function
                callback = query;
                // set query to an empty object
                query = {};
            }

            // if no callback given, just return
            if(typeof(callback) !== 'function'){
                return;
            }

            /* https://github.com/tastejs/todomvc/blob/master/examples/vanillajs/js/store.js#L49 */
            callback.call(this, types.filter(function(category){
                for(var q in query){
                    if(query[q] !== category[q]){
                        // one or more search criteria failed to find a match
                        return false;
                    }
                }
                // all search critera matched
                return true;
            }));
        },
        update: function(type, id, newData, callback){
            callback = callback || function(){};

            // cannot perform an update without an id or new data
            if(!id || !newData){
                return;
            }

            // check for a valid type
            if(type === 'category'){
                types = this.data.categories;
            }
            else if(type === 'item'){
                types = this.data.items;
            }
            else{
                // invalid type
                return;
            }

            /* https://github.com/tastejs/todomvc/blob/master/examples/vanillajs/js/store.js#L85 */
            for(var i = 0; i < types.length; i++){
                if(types[i].id === id){
                    for(var key in newData){
                        types[i][key] = newData[key];
                    }
                }
            }

            callback.call(this, types);

        },
        delete: function(type, id, callback){
            callback = callback || function(){};

            // cannot perform an update without an id
            if(!id){
                return;
            }

            // check for a valid type
            if(type === 'category'){
                types = this.data.categories;
            }
            else if(type === 'item'){
                types = this.data.items;
            }
            else{
                // invalid type
                return;
            }

            /* https://github.com/tastejs/todomvc/blob/master/examples/vanillajs/js/store.js#L116 */
            for(var i = 0; i < types.length; i++){
                if(types[i].id === id){
                    types.splice(i, 1);
                    break;
                }
            }

            callback.call(this, types);
        }
    };

    app.view = {
        render: function(){
            categories = app.model.data.categories;
            items = app.model.data.items;

            categories.forEach(function(category) {
                console.log('- ' + category.name);
                items.forEach(function(item){
                    if(item.category === category.id){
                        console.log('    - ' + item.name);
                    }
                });
            });

            printedHeader = false;
            items.forEach(function(item){
                if(!item.category){
                    if(!printedHeader){
                        console.log('- Uncategorized');
                        printedHeader = true;
                    }
                    console.log('    - ' + item.name);
                }
            });
        },
        show: function(msg, type){
            msg = (msg || '').trim();
            type = (type || '').trim();

            if(msg === ''){
                return;
            }

            switch(type){
                case 'error':
                    console.error('Error: ' + msg);
                    break;
                case 'warning':
                    console.warn('Warning: ' + msg);
                    break;
                default:
                    console.log('Info: ' + msg);
            }
        }
    };

    app.controller = {
        init: function(){
            app.view.render();
        },
        addCategory: function(category){
            category = (category || '').trim();

            if(category === ''){
                app.view.show('invalid category', 'error');
                return;
            }

            app.model.create('category', category, function(){
                app.view.render();
            });
        },
        addItem: function(item, category){
            item = (item || '').trim();
            category = (category || '').trim();

            if(item === ''){
                app.view.show('invalid item', 'error');
                return;
            }

            // first create the item
            app.model.create('item', item, function(itemData){
                if(category === ''){
                    // Item will be uncategorized
                    app.view.render();
                    return;
                }

                // get the Category ID
                app.model.read('category', {name: category}, function(categories){
                    if(categories.length === 0){
                        app.view.show('Category not found. Item will be uncategorized.', 'warning');
                        app.view.render();
                        return;
                    }
                    if(categories.length > 1){
                        app.view.show('Multiple categories found. A random one will be choosen.', 'warning');
                    }

                    // update the item with the found Cateogry ID
                    categoryId = categories[0].id;
                    app.model.update('item', itemData.id, {category: categoryId}, function(){
                        app.view.render();
                    });
                });
            });
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

    /* Start */
    app.controller.init();
})();
