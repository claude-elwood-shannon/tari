use crate::utils::airgapped_signer::{AirgappedSigner, Signature};
use tari_core::transactions::transaction::Transaction;
use tari_crypto::keys::PrivateKey;
use tari_wallet::transaction_service::handle::TransactionServiceHandle;
use std::path::Path;

/// Prepares a transaction for airgapped signing
pub fn prepare_airgapped_transaction(
    transaction_service: &mut TransactionServiceHandle,
    tx_id: u64,
) -> Result<(), String> {
    let transaction = transaction_service.get_transaction(tx_id)?;
    let mut signer = AirgappedSigner::new(transaction.wallet_address);
    signer.prepare_transaction(&transaction)?;
    signer.save_transaction("airgap_tx.dat")?;
    Ok(())
}

/// Submits a signed transaction from airgapped device
pub fn submit_airgapped_transaction(
    transaction_service: &mut TransactionServiceHandle,
    tx_path: &str,
    signature_path: &str,
) -> Result<(), String> {
    let transaction = AirgappedSigner::load_transaction(tx_path)?;
    let signature = std::fs::read_to_string(signature_path)?;
    let signature_bytes = hex::decode(&signature)?;
    
    transaction_service.submit_transaction(
        transaction.body.kernels().first().unwrap().excess_sig.to_hex(),
        &signature_bytes,
        &transaction
    )?;
    Ok(())
}
