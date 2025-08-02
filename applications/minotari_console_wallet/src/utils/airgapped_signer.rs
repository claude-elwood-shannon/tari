use tari_core::transactions::transaction::Transaction;
use tari_crypto::keys::PublicKey;
use tari_utilities::ByteArray;
use tari_wallet::transaction_service::handle::TransactionServiceHandle;
use std::path::Path;

pub struct AirgappedSigner {
    wallet_address: TariAddress,
    transaction_data: Vec<u8>,
}

impl AirgappedSigner {
    pub fn new(wallet_address: TariAddress) -> Self {
        Self {
            wallet_address,
            transaction_data: Vec::new(),
        }
    }

    pub fn prepare_transaction(&mut self, transaction: &Transaction) -> Result<(), String> {
        self.transaction_data = bincode::serialize(transaction)
            .map_err(|e| e.to_string())?;
        Ok(())
    }

    pub fn save_transaction(&self, path: &str) -> Result<(), String> {
        std::fs::write(path, &self.transaction_data)
            .map_err(|e| e.to_string())
    }

    pub fn load_transaction(path: &str) -> Result<Transaction, String> {
        let data = std::fs::read(path)
            .map_err(|e| e.to_string())?;
        bincode::deserialize(&data)
            .map_err(|e| e.to_string())
    }

    pub fn generate_signature(&self, secret_key: &PrivateKey) -> Result<Signature, String> {
        let public_key = PublicKey::from_secret_key(secret_key);
        if !self.wallet_address.is_mine(&public_key) {
            return Err("Invalid secret key for wallet address".to_string());
        }
        
        let signature = Transaction::sign_transaction(&self.transaction_data, secret_key)
            .map_err(|e| e.to_string())?;
        Ok(signature)
    }

    pub fn verify_signature(&self) -> Result<bool, String> {
        let signature = self.generate_signature()?;
        Transaction::verify_signature(&signature)
            .map_err(|e| e.to_string())
    }
}
