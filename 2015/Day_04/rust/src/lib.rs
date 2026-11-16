use md5::{Digest, Md5};

const MAX_ITER: u32 = 100_000_000; // If our loop gets this high something's probably gone wrong

/// Mine some AdventCoin for Santa!
///
/// Return the lowest integer that, when combined with `secret_key`, produces a valid MD5 hash.
///
/// Hashes are checked for validity against the provided checker closure, which is assumed to accept
/// a buffer of bytes representing an MD5 hash and return a boolean.
fn mine_adventcoin<T>(secret_key: &str, checker: T) -> u32
where
    T: Fn([u8; 16]) -> bool,
{
    let secret_key = secret_key.as_bytes();
    let mut hasher = Md5::new();

    for i in 0..MAX_ITER {
        // Load the hasher with the secret key prefix & integer suffix (both to byte strings)
        hasher.update(secret_key);
        hasher.update(i.to_string().as_bytes());

        let output: [u8; 16] = hasher.finalize_reset().into();
        if checker(output) {
            return i;
        }
    }

    0
}

/// Find the AdventCoin hash that has at least 5 leading zeroes
pub fn run_part_one(secret_key: &str) -> u32 {
    // Since we're looking at the hex, we'll need to bitshift to get the 5th character
    // e.g. bytes `000` become hex `00 00 00`, so we get the 5th character by shifting the 3rd byte
    // by 4
    mine_adventcoin(&secret_key, |buffer| {
        u32::from(buffer[0]) + u32::from(buffer[1]) + u32::from(buffer[2] >> 4) == 0
    })
}

/// Find the AdventCoin hash that has at least 6 leading zeroes
pub fn run_part_two(secret_key: &str) -> u32 {
    // Since we're looking at the first 6 characters of the hex, we don't need any bitshift
    mine_adventcoin(&secret_key, |buffer| {
        u32::from(buffer[0]) + u32::from(buffer[1]) + u32::from(buffer[2]) == 0
    })
}
