document.addEventListener('DOMContentLoaded', function() {
    // Função para alternar visibilidade da senha
    function togglePasswordVisibility(inputId, toggleIcon) {
        const passwordInput = document.getElementById(inputId);
        const icon = toggleIcon.querySelector('i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
            toggleIcon.setAttribute('title', 'Ocultar senha');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
            toggleIcon.setAttribute('title', 'Mostrar senha');
        }
    }
    
    // Adicionar botões de mostrar/ocultar senha dinamicamente
    function addPasswordToggleButtons() {
        const passwordFields = [
            'id_password1',
            'id_password2', 
            'id_new_password1',
            'id_new_password2',
            'id_old_password',
            'id_password'
        ];
        
        passwordFields.forEach(fieldId => {
            const passwordInput = document.getElementById(fieldId);
            if (passwordInput && !passwordInput.parentNode.querySelector('.password-toggle')) {
                // Criar botão de toggle
                const toggleButton = document.createElement('button');
                toggleButton.type = 'button';
                toggleButton.className = 'btn btn-outline-secondary password-toggle';
                toggleButton.style.marginLeft = '5px';
                toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
                toggleButton.setAttribute('title', 'Mostrar senha');
                
                // Adicionar evento de clique
                toggleButton.addEventListener('click', function() {
                    togglePasswordVisibility(fieldId, this);
                });
                
                // Inserir após o campo de senha
                passwordInput.parentNode.appendChild(toggleButton);
                
                // Adicionar estilo ao campo de senha
                passwordInput.style.paddingRight = '45px';
            }
        });
    }
    
    // Adicionar validação em tempo real da senha
    function addPasswordValidation() {
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        const newPassword1 = document.getElementById('id_new_password1');
        const newPassword2 = document.getElementById('id_new_password2');
        
        function validatePassword(password) {
            const requirements = {
                length: password.length >= 8,
                uppercase: /[A-Z]/.test(password),
                lowercase: /[a-z]/.test(password),
                number: /[0-9]/.test(password),
                special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
            };
            
            return requirements;
        }
        
        function updatePasswordFeedback(input, requirements) {
            let feedbackElement = input.parentNode.querySelector('.password-feedback');
            if (!feedbackElement) {
                feedbackElement = document.createElement('div');
                feedbackElement.className = 'password-feedback small mt-1';
                input.parentNode.appendChild(feedbackElement);
            }
            
            const feedbackItems = [
                { condition: requirements.length, text: '✓ Mínimo 8 caracteres', bad: '✗ Mínimo 8 caracteres' },
                { condition: requirements.uppercase, text: '✓ Pelo menos 1 letra maiúscula', bad: '✗ Pelo menos 1 letra maiúscula' },
                { condition: requirements.lowercase, text: '✓ Pelo menos 1 letra minúscula', bad: '✗ Pelo menos 1 letra minúscula' },
                { condition: requirements.number, text: '✓ Pelo menos 1 número', bad: '✗ Pelo menos 1 número' },
                { condition: requirements.special, text: '✓ Pelo menos 1 caractere especial', bad: '✗ Pelo menos 1 caractere especial' }
            ];
            
            let allValid = true;
            let feedbackHTML = '<strong>Requisitos da senha:</strong><br>';
            
            feedbackItems.forEach(item => {
                if (item.condition) {
                    feedbackHTML += `<span class="text-success">${item.text}</span><br>`;
                } else {
                    feedbackHTML += `<span class="text-danger">${item.bad}</span><br>`;
                    allValid = false;
                }
            });
            
            feedbackElement.innerHTML = feedbackHTML;
            
            // Atualizar estilo do campo
            if (password.value.length > 0) {
                input.classList.remove('is-valid', 'is-invalid');
                input.classList.add(allValid ? 'is-valid' : 'is-invalid');
            }
        }
        
        // Aplicar validação aos campos de senha
        [password1, password2, newPassword1, newPassword2].forEach(input => {
            if (input) {
                input.addEventListener('input', function() {
                    const requirements = validatePassword(this.value);
                    updatePasswordFeedback(this, requirements);
                    
                    // Validar confirmação de senha
                    if (this.id === 'id_password1' && password2) {
                        const match = this.value === password2.value;
                        password2.classList.remove('is-valid', 'is-invalid');
                        if (password2.value.length > 0) {
                            password2.classList.add(match ? 'is-valid' : 'is-invalid');
                        }
                    }
                    
                    if (this.id === 'id_password2' && password1) {
                        const match = this.value === password1.value;
                        this.classList.remove('is-valid', 'is-invalid');
                        if (this.value.length > 0) {
                            this.classList.add(match ? 'is-valid' : 'is-invalid');
                        }
                    }
                });
            }
        });
    }
    
    // Inicializar quando o DOM estiver pronto
    addPasswordToggleButtons();
    addPasswordValidation();
    
    // Re-inicializar quando houver mudanças no DOM (para forms carregados via AJAX)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                addPasswordToggleButtons();
                addPasswordValidation();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});