import math
from PIL import Image

'''User enters an image size'''
image_size = 1000

def nToCoords(n):
    if n == 0:
        return (0, 0)
    
    # 1. Determine the ring index 'k' 
    # Ring k contains numbers up to (2k+1)^2 - 1
    k = math.ceil((math.sqrt(n + 1) - 1) / 2)
    
    # 2. Find the starting position of the current ring
    prev_max = (2 * k - 1) ** 2 - 1
    pos = n - prev_max  # 1-based index inside the ring
    
    # Each of the 4 sides of ring 'k' has a length of 2k steps
    side = 2 * k
    
    # 0-indexed position within the ring for easier segment grouping
    idx = pos - 1
    segment = idx // side
    remainder = idx % side

    # 3. Map the segment to the exact x, y coordinate
    if segment == 0:    # Right side moving Up
        return (k, -k + 1 + remainder)
    elif segment == 1:  # Top side moving Left
        return (k - 1 - remainder, k)
    elif segment == 2:  # Left side moving Down
        return (-k, k - 1 - remainder)
    else:               # Bottom side moving Right
        return (-k + 1 + remainder, -k)

def coordsToN(coords):
    x, y = coords
    
    # 1. Base case for the origin
    if x == 0 and y == 0:
        return 0
    
    # 2. Determine the ring layer k
    k = max(abs(x), abs(y))
    
    # 3. Calculate the maximum number in the previous ring
    prev_max = (2 * k - 1) ** 2 - 1
    
    # 4. Determine the segment and calculate steps within ring k
    if x == k and y > -k:      # Right side moving Up
        steps = y + k
    elif y == k and x < k:     # Top side moving Left
        steps = 2 * k + (k - x)
    elif x == -k and y < k:    # Left side moving Down
        steps = 4 * k + (k - y)
    else:                      # Bottom side moving Right
        steps = 6 * k + (x + k)
        
    return prev_max + steps

def coordsToPixel(coords, img_Size):
    x, y = coords
    center = img_Size // 2
    return (center + x, center - y)

if image_size % 2 == 0:
    image_size += 1  # Ensure the image size is odd to have a center pixel

def generateMoves(n, img_size, lng, shrt):
    x, y = nToCoords(n)
    moves = set()
    # 8 Knight moves
    knight_moves = [(lng, shrt), (lng, -shrt), (-lng, shrt), (-lng, -shrt), (shrt, lng), (shrt, -lng), (-shrt, lng), (-shrt, -lng)]
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if abs(new_x) <= img_size // 2 and abs(new_y) <= img_size // 2:
            moves.add(coordsToPixel((new_x, new_y), img_size))
    return moves

def createSpiralImage(size, board, output_path):
    """`
    Create a PNG image where each pixel's color is determined by spiral coordinates.
    
    Args:
        size: Odd integer for image dimensions (size x size)
        color_func: Function that takes spiral coordinates (x, y) and returns RGB tuple
        output_path: Path to save the JPG image
    """
    # Create a new RGB image with white background
    img = Image.new('RGB', (size, size), color=(255, 255, 255))
    pixels = img.load()
    
    # Iterate through all pixels using spiral coordinates
    for n in range(size * size):
        x, y = coordsToPixel(nToCoords(n), size)
        if 'b' in board[x][y] or 'R' not in board[x][y]:
            color = (0, 0, 0)  # Black for black knight
        elif 'r' in board[x][y] or 'B' not in board[x][y]:
            color = (255, 0, 0)  # Red for red knight
        else:
            color = (255, 255, 255)  # White for empty

        # Set the pixel
        pixels[x, y] = color
    
    pixels[size // 2, size // 2] = (0, 0, 255)
    # Save as PNG
    img.save(output_path, 'PNG')
    print(f"Image saved to {output_path}")

def createBoard(size, lng, shrt):
    board = [['' for _ in range(size)] for _ in range(size)]
    largest_n = (size * size) - 1
    blackKnight = 0
    redKnight = 1
    turn = 0

    while blackKnight <= largest_n and redKnight <= largest_n:
        if turn == 0:
            x, y = coordsToPixel(nToCoords(blackKnight),size)
            if not ('R' in board[x][y] or 'r' in board[x][y] or 'b' in board[x][y]):
                board[x][y] += 'b'
                moves = generateMoves(blackKnight, size, lng, shrt)
                for dx, dy in moves:
                    if not ('B' in board[dx][dy] or 'r' in board[dx][dy]):
                        board[dx][dy] += 'B'
                turn = (turn + 1) % 2
            blackKnight += 1
        else:
            x, y = coordsToPixel(nToCoords(redKnight), size)
            if not ('B' in board[x][y] or 'r' in board[x][y] or 'b' in board[x][y]):
                board[x][y] += 'r'
                moves = generateMoves(redKnight, size, lng, shrt)
                for dx, dy in moves:
                    if not ('b' in board[dx][dy] or 'R' in board[dx][dy]):
                        board[dx][dy] += 'R'
                turn = (turn + 1) % 2
            redKnight += 1
    return board

for i in range(2, 10):
    for j in range(1, i):
        long_moves, short_moves = i, j
        img_name = f"KM_{long_moves}x{short_moves}.png"
        print(f"Creating image with long moves: {long_moves} and short moves: {short_moves}")
        my_board = createBoard(image_size, long_moves, short_moves)
        createSpiralImage(image_size, my_board, img_name)
