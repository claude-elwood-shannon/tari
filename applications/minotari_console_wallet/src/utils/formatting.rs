// Copyright 2022 The Tari Project
// SPDX-License-Identifier: BSD-3-Clause

use std::fmt;

use tari_core::transactions::transaction::Transaction;
use tari_utilities::hex::Hex;

/// Formats transaction data for airgapped signing
pub struct TransactionFormatter;

impl TransactionFormatter {
    /// Converts transaction to binary format
    pub fn to_binary(transaction: &Transaction) -> Result<Vec<u8>, String> {
        bincode::serialize(transaction).map_err(|e| e.to_string())
    }

    /// Converts transaction to hex string format
    pub fn to_hex_string(transaction: &Transaction) -> Result<String, String> {
        let binary = Self::to_binary(transaction)?;
        Ok(hex::encode(&binary))
    }

    /// Parses signature from hex string
    pub fn parse_signature(signature_hex: &str) -> Result<Vec<u8>, String> {
        hex::decode(signature_hex).map_err(|e| e.to_string())
    }

    /// Formats transaction for display
    pub fn format_transaction_display(transaction: &Transaction) -> Result<String, String> {
        let mut display = String::new();
        
        // Add transaction summary
        writeln!(display, "Transaction ID: {}", transaction.body.kernels().first().map(|k| k.excess_sig.to_hex()).unwrap_or("N/A".to_string()))?;
        writeln!(display, "Inputs: {}", transaction.body.inputs().len())?;
        writeln!(display, "Outputs: {}", transaction.body.outputs().len())?;
        
        // Add detailed breakdown
        writeln!(display, "\n--- Transaction Details ---")?;
        writeln!(display, "Kernels: {:?}", transaction.body.kernels())?;
        writeln!(display, "Inputs: {:?}", transaction.body.inputs())?;
        writeln!(display, "Outputs: {:?}", transaction.body.outputs())?;
        
        Ok(display)
    }
}
