// Function to generate a random salt
async function generateSalt(length = 32) {
    return crypto.getRandomValues(new Uint8Array(length));
}

// Function to derive an AES key from the master password and salt
async function deriveKey(masterPassword, salt, iterations = 100000) {
    const encoder = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
        'raw',
        encoder.encode(masterPassword), // Convert password to byte array
        { name: 'PBKDF2' },
        false,
        ['deriveKey']
    );
    return crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,
            iterations: iterations,
            hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-CBC', length: 256 },
        false,
        ['encrypt', 'decrypt']
    );
}

// Function to encrypt a string (e.g., password, username)
async function encryptString(masterPassword, stringToEncrypt) {
    const salt = await generateSalt();
    const key = await deriveKey(masterPassword, salt);
    const iv = crypto.getRandomValues(new Uint8Array(16)); // Initialization vector (IV)
    const encoder = new TextEncoder();
    const encryptedData = await crypto.subtle.encrypt(
        { name: 'AES-CBC', iv: iv },
        key,
        encoder.encode(stringToEncrypt) // String to encrypt (password or username)
    );
    // Combine salt, IV, and encrypted data for storage
    return {
        salt: Array.from(salt),
        iv: Array.from(iv),
        encryptedData: Array.from(new Uint8Array(encryptedData))
    };
}

// Function to decrypt a string (e.g., password, username)
async function decryptString(masterPassword, encryptedObj) {
    const salt = new Uint8Array(encryptedObj.salt);
    const iv = new Uint8Array(encryptedObj.iv);
    const encryptedData = new Uint8Array(encryptedObj.encryptedData);

    const key = await deriveKey(masterPassword, salt);
    const decryptedData = await crypto.subtle.decrypt(
        { name: 'AES-CBC', iv: iv },
        key,
        encryptedData
    );

    const decoder = new TextDecoder();
    return decoder.decode(decryptedData); // Decrypted string (password or username)
}

// Function to handle encryption for user data
async function encryptUserData(masterPassword, username, password, website) {
    const encryptedPassword = await encryptString(masterPassword, password);
    const encryptedUsername = await encryptString(masterPassword, username);

    return {
        password: encryptedPassword,
        username: encryptedUsername,
        website: website // Website remains a plain string
    };
}

// Function to handle decryption for user data
async function decryptUserData(masterPassword, encryptedData) {
    const decryptedPassword = await decryptString(masterPassword, encryptedData.password);
    const decryptedUsername = await decryptString(masterPassword, encryptedData.username);

    return {
        password: decryptedPassword,
        username: decryptedUsername,
        website: encryptedData.website // Website remains unchanged
    };
}





// Example usage
async function runUserEncryptionDemo() {
    const masterPassword = "my_secure_master_password";
    const username = "my_username";
    const password = "my_website_password";
    const website = "example.com";

    // Encrypt the user data
    const encryptedData = await encryptUserData(masterPassword, username, password, website);
    console.log("Encrypted Data:", JSON.stringify(encryptedData));

    // Simulate storage format: { 'server_username': { ... } }
    const serverData = { 'server_username': encryptedData };
    console.log("Stored JSON Format:", JSON.stringify(serverData));

    // Decrypt the user data
    const decryptedData = await decryptUserData(masterPassword, serverData['server_username']);
    console.log("Decrypted Data:", decryptedData);
}

runUserEncryptionDemo();
