document.addEventListener('DOMContentLoaded', function() {
    const policySelect = document.getElementById('politicas');
    const layerSelect = document.getElementById('layers');
    const ruleSelect = document.getElementById('rules');


    configurarSelecaoUnica('rules');
    configurarSelecaoUnica('layers');
    loadPolicys();
    loadLayers("");
    

    policySelect.addEventListener('change', function() {
        const indexId = this.value;
        if (indexId !== null) {
            loadLayers(indexId);
        }
    });

    
    layerSelect.addEventListener('change', function() {
        const indexId = this.value;
        if (indexId !== null) {
            carregarRegras(indexId);
            carregarTabelaRegras(indexId)
        }
    });


    const button_edit_policy = document.getElementById('button_edit_policy');
    button_edit_policy.addEventListener('click', () => {
        loadModalpolicyLayer(policySelect.value, 'policy', {});
    });

    const button_edit_layer = document.getElementById('button_edit_layer');
    button_edit_layer.addEventListener('click', () => {
        if (layerSelect.value !== ""){
            var association_id = layerSelect.options[layerSelect.selectedIndex].attributes.association_id.value;
        }
        loadModalpolicyLayer(layerSelect.value, 'layer', association_id);
    });

    const button_add_policy = document.getElementById('button_add_policy');
    button_add_policy.addEventListener('click', () => {
        document.getElementById("form-policy-layer-identify").value = 'policy';
    });

    const button_add_layer = document.getElementById('button_add_layer');
    button_add_layer.addEventListener('click', () => {
        document.getElementById("form-policy-layer-identify").value = 'layer';
        if (policySelect.value !== "") {
            loadLayersModalAdd()
            document.getElementById("form-policy-layer-label-layers").hidden = false;
            document.getElementById("form-policy-layer-layers").hidden = false;
            document.getElementById("form-policy-layer-label-name").hidden = true;
            document.getElementById("form-policy-layer-name").hidden = true;
            document.getElementById("form-policy-layer-label-description").hidden = true;
            document.getElementById("form-policy-layer-description").hidden = true;
        }
    });

    const button_edit_rule = document.getElementById('button_edit_rule');
    button_edit_rule.addEventListener('click', () => {
        loadModalRuler(ruleSelect.value, {});
    });

    const button_modal_rule_save = document.getElementById('button-form-rule-save');
    button_modal_rule_save.addEventListener('click', () => {
        editRule()
            .then(() => {
                console.log('Operacao feita com sucesso!');
                carregarRegras(layerSelect.value);
                carregarTabelaRegras(layerSelect.value);
            })
            .catch(error => {
                console.error('Erro ao editar política de camada:', error);
            });
        document.getElementById('close-modal-rule').click();
        
    });

    const button_modal_rule_delete = document.getElementById('button-form-rule-delete');
    button_modal_rule_delete.addEventListener('click', () => {
        var indexId = document.getElementById("form-rule-id").value;
        routes_delete('rule', indexId);
        carregarRegras(layerSelect.value);
        document.getElementById('close-modal-rule').click();
        
    });

    const button_modal_policy_layer_save = document.getElementById('button-form-policy-layer-save');
    button_modal_policy_layer_save.addEventListener('click', () => {
        editPolicyLayer('save')
            .then(() => {
                console.log('policy_layer_save com sucesso!');
                loadLayers(policySelect.value);
            })
            .catch(error => {
                console.error('Erro ao editar política de camada:', error);
            });
        
        document.getElementById('close-modal-policy-layer').click();
    });

    const button_modal_policy_layer_delete = document.getElementById('button-form-policy-layer-delete');
    button_modal_policy_layer_delete.addEventListener('click', () => {
        editPolicyLayer('delete')
            .then(() => {
                console.log('Operacao feita com sucesso!');
                loadLayers(policySelect.value);
            })
            .catch(error => {
                console.error('Erro ao editar política de camada:', error);
            });
        document.getElementById('close-modal-policy-layer').click();
        // window.location.reload();
    });
    


    function loadModalpolicyLayer(indexId, type, association_id) {
        fetch(`http://127.0.0.1:5000/${type}/${indexId}`)
            .then(response => response.json())
            // console.log("Policy_response:", response);
            .then(data => {
                data.forEach(item => {
                    document.getElementById("form-policy-layer-id").value = indexId;
                    document.getElementById("form-policy-layer-association_id").value = association_id;
                    document.getElementById("form-policy-layer-identify").value = item.identify;
                    document.getElementById("form-policy-layer-name").value = item.name;
                    document.getElementById("form-policy-layer-description").value = item.description;
                });
                document.getElementById("button-form-policy-layer-delete").removeAttribute('hidden');
            })
            .catch(error => {
                document.getElementById("form-policy-layer-identify").value = type;
                console.error('Erro ao carregar camadas:', error);
            });
    }

    function loadModalRuler(indexId, association_id) {
        fetch(`http://127.0.0.1:5000/rule/${indexId}`)
            .then(response => response.json())
            // console.log("Policy_response:", response);
            .then(data => {
                data.forEach(item => {
                    document.getElementById("form-rule-id").value = item.rule_id;
                    document.getElementById("form-rule-association_id").value = association_id;
                    document.getElementById("form-rule-identify").value = item.identify;
                    document.getElementById("form-rule-name").value = item.name;
                    document.getElementById("form-rule-code").value = item.code;
                    document.getElementById("form-rule-rule").value = item.rule;
                    document.getElementById("form-rule-description").value = item.description;
                });

                document.getElementById("button-form-rule-delete").removeAttribute('hidden');
                
            })
            .catch(error => {
                document.getElementById("form-rule-identify").value = 'rule';
                console.error('Erro ao carregar camadas:', error);
            });
    }

    function editRule() {
        return new Promise((resolve, reject) => {
            var data = {
                'name': document.getElementById("form-rule-name").value,
                'code': document.getElementById("form-rule-code").value,
                'rule': document.getElementById("form-rule-rule").value,
                'description': document.getElementById("form-rule-description").value
            };
            var indexId = document.getElementById("form-rule-id").value;
            console.log('indexId', indexId)
            if (indexId !== "") {
                routes_alter('rule', indexId, data)
                    .then(data_resp => {
                        console.log('data_resp:', data_resp);
                        resolve(data_resp); // Resolva a Promise com os dados retornados
                    })
                    .catch(error => {
                        console.error('Erro ao editar a regra:', error);
                        reject(error); // Rejeite a Promise com o erro
                    });
            } else {
                routes_add_new('rule', data)
                    .then(data_resp => {
                        console.log('data_resp:', data_resp);
                        resolve(data_resp); // Resolva a Promise com os dados retornados
                    })
                    .catch(error => {
                        console.error('Erro ao adicionar nova regra:', error);
                        reject(error); // Rejeite a Promise com o erro
                    });
            }
        });
    }
    

    function editPolicyLayer(operation) {
        resp = new Promise((resolve, reject) => {
            let data = {
                'name': document.getElementById("form-policy-layer-name").value,
                'description': document.getElementById("form-policy-layer-description").value
            };
            var indexId = document.getElementById("form-policy-layer-id").value;
            var identify = document.getElementById("form-policy-layer-identify").value;
            console.log('indexId', indexId)
            
            if (operation === "delete") {
                if ((identify === "layer") && (policySelect.value !== "")){
                    var association_id = document.getElementById("form-policy-layer-association_id").value;
                    routes_delete('associate-layers-to-policys', association_id)
                        .then(() => resolve())
                        .catch(reject);
                }
                else {
                    routes_delete(identify, indexId)
                        .then(() => resolve())
                        .catch(reject);
                };
                
            }            
            else if (indexId !== "") {
                routes_alter(identify, indexId, data)
                    .then(() => resolve())
                    .catch(reject);
            } else {
                if ((identify === "layer") && (policySelect.value !== "")) {
                    var layer_id = document.getElementById("form-policy-layer-layers").value;
                    data = {
                        'layer_id': layer_id,
                        'policy_id': policySelect.value
                    };
                    routes_add_new('associate-layers-to-policys', data)
                        .then(data_resp => {
                            console.log('data_resp:', data_resp);
                            resolve();
                        })
                        .catch(reject);
                }
                else {
                    routes_add_new(identify, data)
                        .then(data_resp => {
                            console.log('data_resp:', data_resp);
                            resolve();
                        })
                        .catch(reject);
                }
            }
        });
        return resp;
    }

    // Limpe o valor do modal quando fechar
    $('.modal').on('hidden.bs.modal', function (event) {
        var modal = $(this)[0];
        var inputs = modal.querySelectorAll("input, textarea");
        inputs.forEach(function (input) {
            input.value = ""; 
        });
        document.getElementById("button-form-policy-layer-delete").hidden = true;
        document.getElementById("button-form-rule-delete").hidden = true;
        document.getElementById("form-policy-layer-label-layers").hidden = true;
        document.getElementById("form-policy-layer-layers").hidden = true;
        document.getElementById("form-policy-layer-label-name").hidden = false;
        document.getElementById("form-policy-layer-name").hidden = false;
        document.getElementById("form-policy-layer-label-description").hidden = false;
        document.getElementById("form-policy-layer-description").hidden = false;
    });


    function loadPolicys() {
        // Cria um elemento option vazio
        const optionVazia = document.createElement('option');
        optionVazia.value = ''; // Define o valor como vazio
        optionVazia.textContent = 'Selecione a Política Desejada'; // Define o texto como vazio
        policySelect.appendChild(optionVazia); // Adiciona o elemento vazio à lista suspensa
    
        fetch('http://127.0.0.1:5000/policys')
          .then(response => response.json())
          .then(data => {
            // Adicionar opções da resposta da API
            data.forEach(policy => {
                const option = document.createElement('option');
                option.value = policy.policy_id.toString();
                option.textContent = policy.name;
                policySelect.appendChild(option);
            });
          })
          .catch(error => {
            console.error('Erro ao carregar políticas:', error);
          });
      }

    function loadLayers(indexId) {
        limparElemento(layerSelect);
        var url;
        if (indexId === "") {
            url = `http://127.0.0.1:5000/layers`;
        }
        else {
            url = `http://127.0.0.1:5000/associate-layers-to-policys/${indexId}policy_id`;
        };
        fetch(url)
            .then(response => response.json())
            .then(data => {
                
                data.forEach(layer => {
                    let name_layer = "";
                    if (indexId === "") {
                        name_layer = layer.name;
                    }
                    else {
                        name_layer = layer.name_layer;
                    }
                    var params = {
                        'association_id': layer.association_id
                    };
                    const option_layer = criarOption(name_layer, layer.layer_id, params);
                    adicionarFilho(layerSelect, option_layer);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar camadas:', error);
            });

    }

    function carregarRegras(camadaId) {
        const rota1 = `http://127.0.0.1:5000/associate-rules-to-layers/${camadaId}layer_id`;
        const rota2 = 'http://127.0.0.1:5000/rules';

        Promise.all([buscarRuleIDs(rota1), buscarRuleIDs(rota2)])
            .then(([lista1, lista2]) => {
                const diferencas = encontrarDiferencas(lista1, lista2);

                fetch('http://127.0.0.1:5000/rules')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro ao obter os dados da rota.');
                        }
                        return response.json();
                    })
                    .then(data => {

                        limparElemento(ruleSelect);

                        data.forEach(item => {
                            if (diferencas.includes(item.rule_id)) {
                                const option_pen = criarOption(item.name, item.rule_id);
                                adicionarFilho(ruleSelect, option_pen);
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Erro:', error.message);
                    });
            })
            .catch(error => console.error('Erro:', error));
    }

    function carregarTabelaRegras(camadaId) {
        fetch(`http://127.0.0.1:5000/associate-rules-to-layers/${camadaId}layer_id`)
            .then(response => response.json())
            .then(data => {
                const tabelaRegrasRep = document.getElementById('regras_rep');
                const tabelaRegrasPen = document.getElementById('regras_pen');

                limparTabela(tabelaRegrasRep);
                limparTabela(tabelaRegrasPen);

                data.forEach(regra => {
                    const row = criarElemento('tr');
                    row.innerHTML = `<td>${regra.name_rule}</td><td>${regra.action}</td>`;
                    if (regra.action === 'refuse') {
                        adicionarFilho(tabelaRegrasRep.querySelector('tbody'), row);
                    } else if (regra.action === 'pendency') {
                        adicionarFilho(tabelaRegrasPen.querySelector('tbody'), row);
                    }

                    // Adicionar botão de edição
                    const editButton = document.createElement('button');
                    const imgElement = document.createElement('img');
                    imgElement.src = 'img/eye.svg';
                    imgElement.style.width = '15px';
                    imgElement.style.height = '15px';
                    editButton.appendChild(imgElement);
                    
                    editButton.setAttribute("data-toggle", "modal");
                    editButton.setAttribute("data-target", "#meuModal");
                    editButton.setAttribute("value", "valor_desejado");

                    editButton.addEventListener('click', () => {
                        loadModalRuler(regra.rule_id)
                    });
                    const cell_edit = criarElemento('td');
                    cell_edit.style.textAlign = 'center';
                    cell_edit.appendChild(editButton);
                    adicionarFilho(row, cell_edit);


                    // Adicionar botão de exclusão
                    const deleteButton = criarElemento('button');
                    deleteButton.textContent = '\u00D7';
                    deleteButton.style.width = '20px';
                    deleteButton.style.height = '20px';
                    deleteButton.addEventListener('click', () => {
                        excluirRegra(regra.association_id, camadaId);
                        row.remove();
                    });
                    const cell_delete = criarElemento('td');
                    cell_delete.style.textAlign = 'center';
                    cell_delete.appendChild(deleteButton);
                    adicionarFilho(row, cell_delete);

                });
            })
            .catch(error => {
                console.error('Erro ao carregar tabela de regras:', error);
            });
    }

    async function buscarRuleIDs(rota) {
        try {
            const response = await fetch(rota);
            if (!response.ok) {
                throw new Error('Erro ao buscar rule_ids');
            }
            const data = await response.json();
            return data.map(item => item.rule_id);
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    function encontrarDiferencas(lista1, lista2) {
        return lista2.filter(item => !lista1.includes(item));
    }

    function limparTabela(tabela) {
        const tbody = tabela.querySelector('tbody');
        limparElemento(tbody);
    }

    function limparElemento(elemento) {
        elemento.innerHTML = '';
    }

    function criarOption(name, id, params) {
        const option = criarElemento('option');
        option.value = id;
        option.textContent = name;
        if (params && typeof params === 'object' && Object.keys(params).length > 0) {
            for (var key in params) {
                if (params.hasOwnProperty(key)) {
                    option.setAttribute(key, params[key]);
                }
            }
        } 
        return option;
    }

    function criarElemento(tag) {
        return document.createElement(tag);
    }

    function adicionarFilho(pai, filho) {
        pai.appendChild(filho);
    }

    function configurarSelecaoUnica(idSelect) {
        const selectElement = document.getElementById(idSelect);

        selectElement.addEventListener('change', function() {
            for (let i = 0; i < selectElement.options.length; i++) {
                selectElement.options[i].selected = (i === selectElement.selectedIndex);
            }
        });
    }
    
    async function adicionarRegraCamada(event, selectElementId, action) {
        event.preventDefault();
        const selectedRuleId = document.getElementById(selectElementId).value;
        const selectedLayerId = layerSelect.value;
    
        if (selectedRuleId && selectedLayerId) {
            await associarRegraCamada(selectedRuleId, selectedLayerId, action);
            carregarRegras(selectedLayerId);
            carregarTabelaRegras(selectedLayerId);
        } else {
            console.error('Selecione uma regra e uma camada antes de adicionar a associação.');
        }
        
    }
    
    function configurarAdicaoRegra(buttonId, selectElementId, action) {
        const addButton = document.getElementById(buttonId);
    
        // Remove event listener anterior, se existir
        addButton.removeEventListener('click', adicionarRegraCamada);
    
        // Adiciona novo event listener
        addButton.addEventListener('click', function(event) {
            adicionarRegraCamada(event, selectElementId, action);
        });
    }
    
    configurarAdicaoRegra('addRegraPen', 'rules', 'pendency');
    configurarAdicaoRegra('addRegraRep', 'rules', 'refuse');
    
    async function associarRegraCamada(ruleId, layerId, action) {
        try {
            var data = {
                'rule_id': ruleId,
                'layer_id': layerId,
                'action': action
            };
    
            const response = await fetch(`http://127.0.0.1:5000/associate-rules-to-layers`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
    
            if (!response.ok) {
                throw new Error('Erro ao associar regra à camada.');
            }
            console.log('Regra associada com sucesso à camada.');
        } catch (error) {
            console.error('Erro ao associar regra à camada:', error);
        }
    }


    function configurarAdicaoRegra(buttonId, selectElementId, action) {
        const addButton = document.getElementById(buttonId);
    
        // Remove event listener anterior, se existir
        addButton.removeEventListener('click', adicionarRegraCamada);
    
        // Adiciona novo event listener
        addButton.addEventListener('click', function(event) {
            adicionarRegraCamada(event, selectElementId, action);
        });
    }

    function excluirRegra(id, camadaId) {
        fetch(`http://127.0.0.1:5000/associate-rules-to-layers/${id}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao excluir a regra.');
                }
                // Excluído com sucesso
                carregarRegras(camadaId)
            })
            .catch(error => {
                console.error('Erro ao excluir a regra:', error);
            });
    }

    async function routes_add_new(name_route, data_insert) {
        var requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data_insert)
        };
    
        return fetch(`http://127.0.0.1:5000/${name_route}`, requestOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao adicionar nova rota');
                }
                return response.json();
            })
            .then(data => {
                console.log('Inserção feita com sucesso:', data);
                return data;
            })
            .catch(error => {
                console.error('Erro ao adicionar nova rota:', error);
                throw error;
            });
    }

    async function routes_alter(name_route, index_id, data) {
        var requestOptions = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        var queryParams = '';
        for (var key in data) {
            queryParams += `${key}=${encodeURIComponent(data[key])}&`;
        }
        queryParams = queryParams.slice(0, -1);

        return fetch(`http://127.0.0.1:5000/${name_route}/${index_id}?${queryParams}`, requestOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao adicionar nova rota');
                }
                return response.json();
            })
            .then(data => {
                console.log('Inserção feita com sucesso:', data);
                return data;
            })
            .catch(error => {
                console.error('Erro ao adicionar nova Inserção:', error);
                throw error;
            });
    }

    function routes_delete(name_route, index_id) {
        return fetch(`http://127.0.0.1:5000/${name_route}/${index_id}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao adicionar nova rota');
                }
                return response.json();
            })
            .then(data => {
                console.log('Inserção feita com sucesso:', data);
                return data;
            })
            .catch(error => {
                console.error('Erro ao adicionar nova rota:', error);
                throw error;
            });
    }



    const upOrderRuleBtn = document.getElementById('order-up-rule');
    const downOrderRuleBtn = document.getElementById('order-down-rule');
  
    upOrderRuleBtn.addEventListener('click', function() {
      const selectedIndex = layerSelect.selectedIndex;
      if (selectedIndex > 0) {
        const option = layerSelect.options[selectedIndex];
        layerSelect.remove(selectedIndex);
        layerSelect.add(option, selectedIndex - 1);
        

        if (policySelect.value !== ""){
            const itens = buscarItensSelect(layerSelect);
            var data = {
                'prioritys': itens
            };
            console.log(data)
            routes_add_new('associate-layers-to-policys/alter-priority', data)
        }

        
      }
    });
  
    downOrderRuleBtn.addEventListener('click', function() {
      const selectedIndex = layerSelect.selectedIndex;
      if (selectedIndex < layerSelect.options.length - 1) {
        const option = layerSelect.options[selectedIndex];
        layerSelect.remove(selectedIndex);
        layerSelect.add(option, selectedIndex + 1);
      }
    });

    function buscarItensSelect(select) {
        const itensSelect = [];
        for (let i = 0; i < select.options.length; i++) {
            const option = select.options[i];
            const item = {
                'association_id': option.attributes.association_id.value,
                'priority': i
            };
            itensSelect.push(item);
        }
        return itensSelect;
    }


    function loadLayersModalAdd() {
        const rota1 = `http://127.0.0.1:5000/associate-layers-to-policys/${policySelect.value}policy_id`;
        const rota2 = 'http://127.0.0.1:5000/layers';

        Promise.all([buscarLayerIDs(rota1), buscarLayerIDs(rota2)])
            .then(([lista1, lista2]) => {
                const diferencas = encontrarDiferencas(lista1, lista2);
                const selectModalLayer = document.getElementById('form-policy-layer-layers');

                fetch('http://127.0.0.1:5000/layers')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro ao obter os dados da rota.');
                        }
                        return response.json();
                    })
                    .then(data => {

                        limparElemento(selectModalLayer);

                        data.forEach(item => {
                            if (diferencas.includes(item.layer_id)) {
                                const option_layer = criarOption(item.name, item.layer_id);
                                adicionarFilho(selectModalLayer, option_layer);
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Erro:', error.message);
                    });
            })
            .catch(error => console.error('Erro:', error));
    }


    async function buscarLayerIDs(rota) {
        try {
            const response = await fetch(rota);
            if (!response.ok) {
                throw new Error('Erro ao buscar rule_ids');
            }
            const data = await response.json();
            return data.map(item => item.layer_id);
        } catch (error) {
            console.error(error);
            return [];
        }
    }
    
});

