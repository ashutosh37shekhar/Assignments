const {
    Connection,
    Keypair,
    LAMPORTS_PER_SOL,
    clusterApiUrl,
    Transaction,
    SystemProgram,
} = require('@solana/web3.js');
const {
    Token,
    TOKEN_PROGRAM_ID,
} = require('@solana/spl-token');
const {
    TokenSwap,
    TOKEN_SWAP_PROGRAM_ID,
} = require('@solana/spl-token-swap');

const connection = new Connection(clusterApiUrl('mainnet-beta'), 'confirmed');

// Replace these with actual values
const wallet = Keypair.fromSecretKey(Uint8Array.from([])); // Your wallet secret key
const swapPublicKey = new PublicKey(''); // Token swap public key
const fromTokenMint = new PublicKey(''); // Mint address of token to swap from
const toTokenMint = new PublicKey(''); // Mint address of token to swap to
const amountIn = 1000000; // Amount to swap in

async function swapTokens() {
const swapAccountInfo = await TokenSwap.load(
        connection,
        swapPublicKey,
        TOKEN_SWAP_PROGRAM_ID,
        wallet
    );

    const fromToken = new Token(
        connection,
        fromTokenMint,
        TOKEN_PROGRAM_ID,
        wallet
    );

    const toToken = new Token(
        connection,
        toTokenMint,
        TOKEN_PROGRAM_ID,
        wallet
    );

    const swapTransaction = await swapAccountInfo.swap({
        amountIn,
        fromTokenAccount: await fromToken.getOrCreateAssociatedAccountInfo(wallet.publicKey),
        toTokenAccount: await toToken.getOrCreateAssociatedAccountInfo(wallet.publicKey),
        owner: wallet.publicKey,
    });
    const signature = await connection.sendTransaction(swapTransaction, [wallet]);
        await connection.confirmTransaction(signature);

        console.log('Swap transaction sent:', signature);
    }

    swapTokens().catch(err => {
        console.error('Error swapping tokens:', err);
});
    
    // npm install @solana/web3.js @solana/spl-token @solana/spl-token-swap