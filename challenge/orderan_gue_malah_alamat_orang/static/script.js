let currentUser = null;
let currentOrder = null;
let allProducts = [];
let userAddress = null; // Store user's address fetched from backend
let messageTimeout;

// Utility function to display on-page messages
function displayMessage(message, type = 'info', duration = 5000) {
    const msgDisplay = document.getElementById('appMessageDisplay');
    if (!msgDisplay) return;

    // Clear previous timeout
    clearTimeout(messageTimeout);

    // Reset classes
    msgDisplay.className = 'app-message-display';
    msgDisplay.style.display = 'none'; // Hide before showing to reset animation/state

    msgDisplay.textContent = message;
    msgDisplay.classList.add('active'); // For animation
    msgDisplay.style.display = 'block';

    if (type === 'error') {
        msgDisplay.classList.add('message-error');
    } else if (type === 'success') {
        msgDisplay.classList.add('message-success');
    } else {
        msgDisplay.classList.add('message-info');
    }

    messageTimeout = setTimeout(() => {
        msgDisplay.classList.remove('active');
        msgDisplay.style.display = 'none';
        msgDisplay.textContent = '';
        msgDisplay.className = 'app-message-display'; // Clear type classes
    }, duration);
}

// Utility function to show/hide sections
function showSection(sectionId) {
    // Update navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        // Check if onclick contains the sectionId or if it's explicitly 'all' for products
        if (btn.onclick.toString().includes(`showSection('${sectionId}')`)) {
             btn.classList.add('active');
        } else {
             btn.classList.remove('active');
        }
    });

    // Hide all main content sections
    document.querySelectorAll('#mainContent > div').forEach(div => {
        div.classList.remove('active');
    });
    // Show the target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Specific logic for order history when section is shown
    if (sectionId === 'orderHistory' && currentUser) {
        loadOrderHistory();
    }
    // Specific logic for products when section is shown
    if (sectionId === 'products' && currentUser) {
        loadProducts(); // Reload products to potentially update address warning
    }
}

// Function to format price
function formatPrice(priceString) {
    // Remove "Rp " and dots if present, then convert to number
    const numericPrice = parseInt(priceString.toString().replace('Rp ', '').replace(/\./g, ''));
    if (isNaN(numericPrice)) {
        return priceString; // Return original if cannot parse
    }
    return numericPrice.toLocaleString('id-ID');
}

// New internal function for client-side state cleanup
function _clearClientState() {
    currentUser = null;
    userAddress = null; // Clear address on logout
    document.getElementById('userInfo').classList.remove('active');
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('login').classList.add('active');
    document.getElementById('loginForm').reset();
    document.getElementById('welcomeMessage').innerHTML = `
        <h2>Selamat Datang di IT Club Tech Store!</h2>
        <p>Temukan peralatan IT, pentesting, dan komponen rakitan terbaik dengan harga kompetitif</p>
    `;
    // Clear product grid and order history display
    document.getElementById('productGrid').innerHTML = '';
    document.getElementById('orderHistoryBody').innerHTML = '';
    document.getElementById('emptyHistory').style.display = 'block';
}

// --- API Interaction Functions ---

async function fetchApi(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include' // Send cookies (session)
    };
    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);
    // Even if !response.ok, try to parse JSON to get error message
    const json = await response.json().catch(() => ({ message: 'Unknown error', status: response.status }));
    
    if (!response.ok) {
        const error = new Error(json.message || 'API request failed');
        error.status = response.status; // Attach status for specific handling
        
        // Only display error for non-401 errors, as 401 on initial load is handled silently
        if (error.status !== 401) {
            displayMessage('API Error: ' + error.message, 'error');
        }
        
        // If 401, trigger silent client-side cleanup
        if (error.status === 401) {
            _clearClientState(); 
        }
        throw error;
    }
    return json;
}

// --- Login/Logout ---

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        displayMessage('Silakan isi nama pengguna dan kata sandi.', 'error');
        return;
    }

    try {
        const response = await fetchApi('/login', 'POST', { username, password });
        currentUser = response.user;
        
        // Update UI
        document.getElementById('usernameDisplay').textContent = currentUser.username;
        document.getElementById('userInfo').classList.add('active');
        document.getElementById('welcomeMessage').innerHTML = `
            <h2>Selamat Datang, ${currentUser.username}!</h2>
            <p>Nikmati belanja peralatan IT, pentesting, dan komponen rakitan terbaik dengan harga spesial</p>
        `;
        
        // Show main content
        document.getElementById('login').classList.remove('active');
        document.getElementById('mainContent').style.display = 'block';
        
        // Fetch products and address for the logged-in user
        await loadAddress(); // Load address first
        await loadProducts(); // Then products, as products might depend on address status
        showSection('products');
        displayMessage('Login berhasil!', 'success');

    } catch (error) {
        console.error('Login Failed:', error.message);
        displayMessage('Login Failed: ' + error.message, 'error');
    }
});

async function logout(confirmLogout = true) {
    if (confirmLogout && !confirm('Apakah Anda yakin ingin logout?')) {
        return;
    }
    
    try {
        await fetchApi('/logout', 'POST');
        displayMessage('Anda telah berhasil logout.', 'info');
    } catch (error) {
        console.error('Logout API call failed:', error.message);
        // Do not displayMessage for 401 during logout, as it's already handled by _clearClientState()
        // and we don't want redundant messages
        if (error.status !== 401) {
            displayMessage('Logout Failed: ' + error.message, 'error');
        }
    } finally {
        _clearClientState(); // Always clear client-side state after attempting API call
    }
}

// --- User Info & Address Management ---

async function loadUserInfo() {
    try {
        const response = await fetchApi('/api/user_info', 'GET');
        currentUser = response.user;
        document.getElementById('usernameDisplay').textContent = currentUser.username;
        document.getElementById('userInfo').classList.add('active');
        document.getElementById('welcomeMessage').innerHTML = `
            <h2>Selamat Datang, ${currentUser.username}!</h2>
            <p>Nikmati belanja peralatan IT, pentesting, dan komponen rakitan terbaik dengan harga spesial</p>
        `;
        document.getElementById('mainContent').style.display = 'block';
    } catch (error) {
        // If it's a 401, _clearClientState() has already been called by fetchApi
        // so we just log and ensure login form is visible.
        if (error.status === 401) {
            console.log('User not logged in or session expired, showing login form.');
        } else {
            console.error('Failed to load user info:', error.message);
            displayMessage('Failed to load user info: ' + error.message, 'error');
        }
    }
}

async function loadAddress() {
    if (!currentUser) return; // Should not happen if API is working correctly
    try {
        const response = await fetchApi('/api/manage_address', 'GET');
        userAddress = response.address;
        console.log('User address loaded for pre-fill:', userAddress);
    } catch (error) {
        // Silently handle "Address not found" (404) or other errors, just means userAddress remains null
        userAddress = null;
        console.log('No address found for current user or error fetching address: ', error.message);
    }
}

// Address management is no longer a separate UI section, form elements are used in order form directly
/*
document.getElementById('addressForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    // This part is removed as address is handled in order process
});
*/

// --- Product List ---

async function loadProducts() {
    if (!currentUser) return;
    try {
        const response = await fetchApi('/api/products', 'GET');
        allProducts = response.products.map(p => ({
            ...p,
            // Ensure price is stored as a number for calculations, keep original string for display if needed
            price: parseInt(p.price.toString().replace('Rp ', '').replace(/\./g, '')) 
        }));
        
        // Welcome message is now generic
        document.getElementById('welcomeMessage').innerHTML = `
            <h2>Selamat Datang, ${currentUser.username}!</h2>
            <p>Temukan peralatan IT, pentesting, dan komponen rakitan terbaik dengan harga spesial</p>
        `;

        renderProducts(allProducts);
        // Ensure filters are reset or applied correctly on load
        filterProducts('all', document.querySelector(".category-filter button[data-category='all']") || document.querySelector(".category-filter button.active"));

    } catch (error) {
        console.error('Failed to load products:', error.message);
        displayMessage('Gagal memuat produk: ' + error.message, 'error');
    }
}

function renderProducts(productsToRender) {
    const productGrid = document.getElementById('productGrid');
    productGrid.innerHTML = ''; // Clear existing products

    productsToRender.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product';
        productDiv.dataset.category = product.category;
        productDiv.innerHTML = `
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="product-content">
                <span class="category-label ${product.category}-category">${product.category.toUpperCase()}</span>
                <h3>${product.name}</h3>
                <div class="product-description">${product.description}</div>
                <div class="product-price">
                    <div class="price-label">HARGA</div>
                    <div class="price-value">Rp ${formatPrice(product.price.toString())}</div>
                </div>
                <button onclick="orderProduct(${product.id}, '${product.name}', ${product.price})"><i class="fas fa-shopping-cart"></i> Pesan Sekarang</button>
            </div>
        `;
        productGrid.appendChild(productDiv);
    });
    // This assumes the active button exists; safer to pass category directly or re-evaluate
    updateProductCount(productsToRender.length, document.querySelector('.category-filter button.active')?.dataset.category || 'all');
}


// --- Product Filtering ---
let currentFilteredProducts = [];

function initializeProductsFiltering() {
    // No need to set allProducts = allProducts;
    renderProducts(allProducts); // Render all products initially
    updateProductCount(allProducts.length, 'all');
    // Ensure 'all' button is active by default
    document.querySelector(".category-filter button[data-category='all']")?.classList.add('active');
}

function filterProducts(category, element) {
    // Update active button
    document.querySelectorAll('.category-filter button').forEach(btn => {
        btn.classList.remove('active');
    });
    if (element) element.classList.add('active');
    
    currentFilteredProducts = allProducts.filter(product => {
        return category === 'all' || product.category === category;
    });
    renderProducts(currentFilteredProducts);
    updateProductCount(currentFilteredProducts.length, category);
}

function updateProductCount(count, category) {
    let categoryName = '';
    switch(category) {
        case 'pentesting': categoryName = 'Alat Pentesting'; break;
        case 'pc-build': categoryName = 'Rakitan PC'; break;
        case 'iot': categoryName = 'IoT'; break;
        case 'security': categoryName = 'Keamanan'; break;
        case 'programming': categoryName = 'Programming'; break;
        case 'networking': categoryName = 'Jaringan'; break;
        case 'software': categoryName = 'Software'; break; 
        case 'accessories': categoryName = 'Aksesoris'; break; 
        default: categoryName = '';
    }
    
    document.getElementById('productCount').textContent = `Menampilkan ${count} produk ${categoryName}`;
}

// --- Order Process ---

async function orderProduct(productId, itemName, itemPrice) {
    if (!currentUser) {
        displayMessage('Anda harus login untuk memesan produk.', 'error');
        showSection('login');
        return;
    }
    // Address is now entered directly in the order form, no pre-check needed here
    // But we need to ensure address input fields are filled before confirming
    
    currentOrder = { 
        productId: productId,
        item: itemName, 
        price: itemPrice,
        // The address and phone are for pre-filling the order form, if userAddress exists
        addressDetails: userAddress ? `${userAddress.street}, ${userAddress.city}, ${userAddress.postal_code}` : '',
        phone: userAddress ? userAddress.phone : ''
    };
    
    // Pre-fill address and phone fields as empty for user to input
    document.getElementById('orderAddressInput').value = '';
    document.getElementById('orderPhoneInput').value = '';

    document.getElementById('orderItemDisplay').innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
            <i class="fas fa-shopping-cart" style="font-size: 2em; color: #667eea;"></i>
            <div style="text-align: left;">
                <div style="font-size: 1.2em; font-weight: 900; color: #333;">${itemName}</div>
                <div style="font-size: 1.5em; font-weight: 900; color: #764ba2; margin-top: 5px;">
                    Rp ${formatPrice(itemPrice.toString())}
                </div>
            </div>
        </div>
    `;
    
    // Attempt to fetch order details from backend (vulnerable step for IDOR display)
    try {
        // IMPORTANT: Sending currentUser.id as user_id. This is where the client-side manipulation happens.
        // Attacker would change `currentUser.id` to another user's ID using browser dev tools or proxy.
        const orderPreviewResponse = await fetchApi('/api/order', 'POST', {
            product_id: productId,
            user_id: currentUser.id // VULNERABLE: This is taken directly from currentUser, can be manipulated
        });

        const productDetails = orderPreviewResponse.product;
        const shippingAddress = orderPreviewResponse.shipping_address;
        const targetUserId = orderPreviewResponse.target_user_id;
        const flag = orderPreviewResponse.flag;

        // Update the current order with full details from backend for checkout
        currentOrder.fullProductDetails = productDetails;
        currentOrder.shippingAddressDetails = shippingAddress;
        currentOrder.targetUserId = targetUserId;
        currentOrder.flag = flag;

        // Display flag if present
        const flagMessageDiv = document.getElementById('flagMessageDiv');
        if (flag) {
            flagMessageDiv.innerHTML = `
                <h3>PENTING: Temuan Kerentanan!</h3>
                <p>Anda berhasil memicu kerentanan IDOR. Flag Anda adalah:</p>
                <div class="flag-box">
                    <code>${flag}</code>
                </div>
                <p>Silakan laporkan temuan ini kepada tim keamanan. Sementara itu, order di bawah akan tetap diproses ke alamat yang dipilih (yang rentan).</p>
            `;
            flagMessageDiv.style.display = 'block';
        } else {
            flagMessageDiv.style.display = 'none';
        }

        // Display warning if address is not current user's
        const orderAddressWarning = document.getElementById('orderAddressWarning');
        if (targetUserId !== currentUser.id) {
            orderAddressWarning.innerHTML = `
                <strong>PERHATIAN:</strong> Alamat ini bukan milik akun Anda yang sedang login. Ini adalah alamat milik User ID: ${targetUserId}.
                Ini adalah contoh dari Insecure Direct Object Reference (IDOR) dimana backend tidak memvalidasi ownership dari alamat yang digunakan.
            `;
            orderAddressWarning.style.display = 'block';
        } else {
            orderAddressWarning.style.display = 'none';
        }
        
        // Frontend will leave the fields empty for user input, even if backend found an address.
        // document.getElementById('orderAddressInput').value = `${shippingAddress.street}, ${shippingAddress.city}, ${shippingAddress.postal_code}`;
        // document.getElementById('orderPhoneInput').value = shippingAddress.phone || '';


        showSection('order');

    } catch (error) {
        // If the error code is TARGET_USER_NO_ADDRESS, alert user
        if (error.status === 400 && error.message.includes("TARGET_USER_NO_ADDRESS")) {
            displayMessage('User ID target tidak memiliki alamat terdaftar. Tidak dapat memproses order.', 'error');
            showSection('products'); // Go back to products
        }
        else if (error.message === "Unauthorized. Please log in.") {
            displayMessage("Sesi Anda telah berakhir. Silakan login kembali.", 'error');
            _clearClientState(); 
        } else {
            displayMessage('Gagal mengambil detail order: ' + error.message, 'error');
        }
        console.error('Error in orderProduct:', error);
    }
}


async function checkout() {
    if (!currentUser || !currentOrder) {
        displayMessage('Informasi order tidak lengkap. Silakan coba lagi.', 'error');
        return;
    }

    const address = document.getElementById('orderAddressInput').value;
    const phone = document.getElementById('orderPhoneInput').value;
    
    if (!address || !phone) {
        displayMessage('Silakan lengkapi semua informasi pengiriman (alamat dan nomor telepon).', 'error');
        return;
    }

    try {
        const confirmResponse = await fetchApi('/api/confirm_order', 'POST', {
            product_id: currentOrder.productId,
            target_user_id: currentOrder.targetUserId, // The (potentially IDOR'd) user ID
            address_details: address,
            phone_number: phone
        });

        // Update checkout display
        document.getElementById('receiverName').textContent = currentUser.username; // Logged in user's name
        document.getElementById('accountId').textContent = currentUser.id;
        document.getElementById('phoneNumber').textContent = phone;
        document.getElementById('deliveryAddress').textContent = address;
        document.getElementById('itemName').textContent = currentOrder.item;
        document.getElementById('itemPrice').textContent = formatPrice(currentOrder.price.toString());
        document.getElementById('orderNum').textContent = confirmResponse.order_id; // From backend response
        
        showSection('checkout');
        displayMessage('Pesanan Anda berhasil ditempatkan!', 'success');
        
        // Update order history display
        loadOrderHistory();
    } catch (error) {
        console.error('Checkout failed:', error.message);
        displayMessage('Gagal menyelesaikan pembayaran: ' + error.message, 'error');
    }
}

function backToProducts() {
    showSection('products');
}

// --- Order History ---

async function loadOrderHistory() {
    if (!currentUser) return;
    try {
        const response = await fetchApi('/api/order_history', 'GET');
        const orders = response.orders; // Assuming API returns orders for currentUser
        
        const orderHistoryBody = document.getElementById('orderHistoryBody');
        const emptyHistory = document.getElementById('emptyHistory');
        
        if (orders && orders.length > 0) {
            orderHistoryBody.innerHTML = '';
            emptyHistory.style.display = 'none';
            
            orders.forEach(order => {
                let statusClass = 'status-pending';
                let statusText = 'Menunggu';
                
                if (order.status === 'delivered') {
                    statusClass = 'status-delivered';
                    statusText = 'Terkirim';
                } else if (order.status === 'shipped') {
                    statusClass = 'status-shipped';
                    statusText = 'Dikirim';
                }
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${order.id}</strong></td>
                    <td>${order.date}</td>
                    <td>${order.product}</td>
                    <td><strong>Rp ${formatPrice(order.price.toString())}</strong></td>
                    <td>${order.shipping_address}<br>(${order.recipient_username}, ID: ${order.shipping_to_user_id})</td>
                    <td><span class="${statusClass}">${statusText}</span></td>
                `;
                orderHistoryBody.appendChild(row);
            });
        } else {
            orderHistoryBody.innerHTML = '';
            emptyHistory.style.display = 'block';
        }
    } catch (error) {
        console.error('Failed to load order history:', error.message);
        displayMessage('Gagal mengambil riwayat pesanan.', 'error');
        document.getElementById('orderHistoryBody').innerHTML = '';
        document.getElementById('emptyHistory').style.display = 'block';
    }
}

function viewOrderDetails(orderId) {
    // This currently re-fetches all orders to find one. For a real app, pass details or fetch specific.
    fetchApi('/api/order_history', 'GET').then(response => {
        const order = response.orders.find(o => o.id === orderId);
        if (order) {
            // Using displayMessage for details might overflow or be unreadable. Keep original alert or show in modal.
            // Sticking with alert for now as it's a specific, user-initiated action and not disruptive flow-wise.
            alert(
                `Detail Pesanan:\n\n` +
                `No. Pesanan: ${order.id}\n` +
                `Tanggal: ${order.date}\n` +
                `Produk: ${order.product}\n` +
                `Harga: Rp ${formatPrice(order.price.toString())}\n` +
                `Status: ${order.status === 'pending' ? 'Menunggu' : order.status === 'shipped' ? 'Dikirim' : 'Terkirim'}\n` +
                `Alamat: ${order.shipping_address}\n` +
                `Telepon: ${order.phone_number}\n` +
                `Pengiriman ke User ID: ${order.shipping_to_user_id} (${order.recipient_username})`
            );
        } else {
            displayMessage('Detail pesanan tidak ditemukan.', 'error');
        }
    }).catch(error => {
        console.error('Error fetching order details:', error);
        displayMessage('Gagal mengambil detail pesanan.', 'error');
    });
}

// --- Initialize on page load ---

window.addEventListener('DOMContentLoaded', async function() {
    // Check if user is already logged in via session (Flask)
    await loadUserInfo();
    if (currentUser) {
        // If logged in, load products and order history
        await loadProducts();
        await loadAddress(); // Only load address if logged in, for pre-fill
        showSection('products'); // Default view after login
    } else {
        // If not logged in, show login form
        showSection('login');
    }
});