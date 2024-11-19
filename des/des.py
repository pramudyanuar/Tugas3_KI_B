from des.desTables import *

def str_to_bin(user_input):
    
        # Convert the string to binary
        binary_representation = ''
        
        for char in user_input:
            # Get ASCII value of the character and convert it to binary
            binary_char = format(ord(char), '08b')
            binary_representation += binary_char
            binary_representation = binary_representation[:64]
        
        # Pad or truncate the binary representation to 64 bits
        binary_representation = binary_representation[:64].ljust(64, '0')
        
        # Print the binary representation
        # print("Binary representation of input string: ", binary_representation)
        # print(len(binary_representation), 'bits of input string')
        
        return binary_representation

def binary_to_ascii(binary_str):
    ascii_str = ''.join([chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)])
    return ascii_str

def binary_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:].zfill(16)
    return hex_str

def hex_to_binary(hex_str):
    binary_str = bin(int(hex_str, 16))[2:].zfill(64)
    return binary_str

def ip_on_binary_rep(binary_representation):
    
    ip_result = [None] * 64
    
    for i in range(64):
        ip_result[i] = binary_representation[ip_table[i] - 1]

    # Convert the result back to a string for better visualization
    ip_result_str = ''.join(ip_result)
    
    return ip_result_str

def key_in_binary_conv(keys):
    # Original key (can be changed but it should be 8 char)
    binary_representation_key = ''
    
    for char in keys:
    # Convert the characters to binary and concatenate to form a 64-bit binary string
        binary_key = format(ord(char), '08b') 
        binary_representation_key += binary_key

    
    return binary_representation_key

def generate_round_keys(keys):
    
    # Key into binary
    binary_representation_key = key_in_binary_conv(keys)
    pc1_key_str = ''.join(binary_representation_key[bit - 1] for bit in pc1_table)

    
    # Split the 56-bit key into two 28-bit halves
    c0 = pc1_key_str[:28]
    d0 = pc1_key_str[28:]
    round_keys = []
    for round_num in range(16):
        # Perform left circular shift on C and D
        c0 = c0[shift_schedule[round_num]:] + c0[:shift_schedule[round_num]]
        d0 = d0[shift_schedule[round_num]:] + d0[:shift_schedule[round_num]]
        # Concatenate C and D
        cd_concatenated = c0 + d0

        # Apply the PC2 permutation
        round_key = ''.join(cd_concatenated[bit - 1] for bit in pc2_table)

        # Store the round key
        round_keys.append(round_key)
    return round_keys

def encryption(user_input, keys):
    binary_rep_of_input = str_to_bin(user_input)
    # Initialize lists to store round keys
    round_keys = generate_round_keys(keys)

    ip_result_str = ip_on_binary_rep(binary_rep_of_input)

    # the initial permutation result is devided into 2 halfs
    lpt = ip_result_str[:32]
    rpt = ip_result_str[32:]



    # Assume 'rpt' is the 32-bit right half, 'lpt' is the 32-bit left half, and 'round_keys' is a list of 16 round keys

    for round_num in range(16):
        # Perform expansion (32 bits to 48 bits)
        expanded_result = [rpt[i - 1] for i in e_box_table]

        # Convert the result back to a string for better visualization
        expanded_result_str = ''.join(expanded_result)

        # Round key for the current round
        round_key_str = round_keys[round_num]


        xor_result_str = ''
        for i in range(48):
            xor_result_str += str(int(expanded_result_str[i]) ^ int(round_key_str[i]))


        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_result_str[i:i+6] for i in range(0, 48, 6)]

        # Initialize the substituted bits string
        s_box_substituted = ''

        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            # Extract the row and column bits
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)

            # Lookup the S-box value
            s_box_value = s_boxes[i][row_bits][col_bits]
            
            # Convert the S-box value to a 4-bit binary string and append to the result
            s_box_substituted += format(s_box_value, '04b')

        # Apply a P permutation to the result
        p_box_result = [s_box_substituted[i - 1] for i in p_box_table]

        # # Convert the result back to a string for better visualization
        # p_box_result_str = ''.join(p_box_result)


        # Convert LPT to a list of bits for the XOR operation
        lpt_list = list(lpt)

        # Perform XOR operation
        new_rpt = [str(int(lpt_list[i]) ^ int(p_box_result[i])) for i in range(32)]

        # Convert the result back to a string for better visualization
        new_rpt_str = ''.join(new_rpt)

        # Update LPT and RPT for the next round
        lpt = rpt
        rpt = new_rpt_str

        # Print or use the RPT for each round

    # At this point, 'lpt' and 'rpt' contain the final left and right halves after 16 rounds

    # After the final round, reverse the last swap
    final_result = rpt + lpt

    # Perform the final permutation (IP-1)
    final_cipher = [final_result[ip_inverse_table[i] - 1] for i in range(64)]

    # Convert the result back to a string for better visualization
    final_cipher_str = ''.join(final_cipher)

    # Print or use the final cipher(binary)
    # print("Final Cipher binary:", final_cipher_str, len(final_cipher_str))


    # Convert binary cipher to ascii
    # final_cipher_ascii = binary_to_ascii(final_cipher_str)
    final_cipher = binary_to_hex(final_cipher_str)
    
    return final_cipher

# decryption of cipher to origional

def decryption(final_cipher, keys):
    
    cipher_text = hex_to_binary(final_cipher)
    # Initialize lists to store round keys
    round_keys = generate_round_keys(keys)
    
    # Apply Initial Permutation
    ip_dec_result_str = ip_on_binary_rep(cipher_text)
    
    lpt = ip_dec_result_str[:32]
    rpt = ip_dec_result_str[32:]

    for round_num in range(16):
        # Perform expansion (32 bits to 48 bits)
        expanded_result = [rpt[i - 1] for i in e_box_table]
    
        # Convert the result back to a string for better visualization
        expanded_result_str = ''.join(expanded_result)
        # print(expanded_result_str)
        # Round key for the current round
        round_key_str = round_keys[15-round_num]
    
        # XOR between key and expanded result 
        xor_result_str = ''
        for i in range(48):
            xor_result_str += str(int(expanded_result_str[i]) ^ int(round_key_str[i]))
    
    
        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_result_str[i:i+6] for i in range(0, 48, 6)]
    
        # Initialize the substituted bits string
        s_box_substituted = ''
    
        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            # Extract the row and column bits
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)
    
            # Lookup the S-box value
            s_box_value = s_boxes[i][row_bits][col_bits]
            
            # Convert the S-box value to a 4-bit binary string and append to the result
            s_box_substituted += format(s_box_value, '04b')
    
        # Apply a P permutation to the result
        p_box_result = [s_box_substituted[i - 1] for i in p_box_table]
    
        # Convert the result back to a string for better visualization
        # p_box_result_str = ''.join(p_box_result)
    
        # Convert LPT to a list of bits for the XOR operation
        lpt_list = list(lpt)
    
        # Perform XOR operation
        new_rpt = [str(int(lpt_list[i]) ^ int(p_box_result[i])) for i in range(32)]
    
        # Convert the result back to a string for better visualization
        new_rpt_str = ''.join(new_rpt)
    
        # Update LPT and RPT for the next round
        lpt = rpt
        rpt = new_rpt_str
    
        # Print or use the RPT for each round
    
    final_result = rpt + lpt
    # Perform the final permutation (IP-1)
    final_cipher = [final_result[ip_inverse_table[i] - 1] for i in range(64)]

    # Convert the result back to a string for better visualization
    final_cipher_str = ''.join(final_cipher)

    # Print or use the final cipher

    # binary cipher string to ascii
    final_cipher_ascii = binary_to_ascii(final_cipher_str)

    return final_cipher_ascii

def encryption_text(user_input, keys):
    while len(user_input) % 8 != 0:
        user_input += ' '

    cipher_text = ""
    for i in range(0, len(user_input), 8):
        cipher_text += encryption(user_input[i:i+8], keys)

    return cipher_text

def decryption_text(cipher_text, keys):

    final_text = ""
    for i in range(0, len(cipher_text), 16):
        final_text += decryption(cipher_text[i:i+16], keys)

    return final_text.strip()