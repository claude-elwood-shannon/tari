// Copyright 2022 The Tari Project
// SPDX-License-Identifier: BSD-3-Clause

use std::fs::File;
use std::io::Write;
use std::path::Path;

use tari_common_types::tari_address::TariAddress;
use tari_core::transactions::transaction::Transaction;
use tari_utilities::hex::Hex;

/// Structure for handling airgapped transaction signing
/// Stores wallet address, transaction data and signature information
pub struct AirgappedSigner {
    pub wallet_address: TariAddress,
    pub transaction_data: Vec<u8>,
    pub signature_file: String,
}

impl AirgappedSigner {
    /// Creates a new AirgappedSigner instance
    /// 
    /// # Arguments
    /// * `wallet_address` - Wallet address to use
    pub fn new(wallet_address: TariAddress) -> Self {
        Self {
            wallet_address,
            transaction_data: Vec::new(),
            signature_file: String::new(),
        }
    }

    /// Prepares transaction data for signing
    /// 
    /// # Arguments
    /// * `transaction` - Transaction to prepare
    pub fn prepare_transaction(&mut self, transaction: &Transaction) -> Result<(), String> {
        self.transaction_data = transaction.to_binary().map_err(|e| e.to_string())?;
        Ok(())
    }

    /// Saves transaction data to a file
    /// 
    /// # Arguments
    /// * `path` - File path to save the transaction
    pub fn save_transaction(&self, path: &str) -> Result<(), String> {
        let transaction_hex = hex::encode(&self.transaction_data);
        let mut file = File::create(path).map_err(|e| e.to_string())?;
        file.write_all(transaction_hex.as_bytes()).map_err(|e| e.to_string())?;
        Ok(())
    }

    /// Loads a signature from a file
    /// 
    /// # Arguments
    /// * `path` - Path to the signature file
    pub fn load_signature(&mut self, path: &str) -> Result<(), String> {
        let signature_hex = std::fs::read_to_string(path).map_err(|e| e.to_string())?;
        self.signature_file = signature_hex;
        Ok(())
    }

    /// Verifies the transaction signature
    pub fn verify_signature(&self) -> Result<bool, String> {
        if self.signature_file.is_empty() {
            return Ok(false);
        }

        let signature_bytes = hex::decode(&self.signature_file).map_err(|e| e.to_string())?;
        let signature = self.wallet_address
            .verify_signature(&signature_bytes, &self.transaction_data)
            .map_err(|e| e.to_string())?;
        
        Ok(signature)
    }
}
