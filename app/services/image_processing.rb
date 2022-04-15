class ImageProcessing
  def call
    img = Magick::Image.read("input.png").first
    pixels = img.get_pixels(0,0,img.columns,img.rows)

    rgbs = {}

    for pixel in pixels
      rgbs["#{pixel.red} #{pixel.green} #{pixel.blue}"] ||= 0
      rgbs["#{pixel.red} #{pixel.green} #{pixel.blue}"] += 1
    end

    rgbs

    # img.store_pixels(0,0, img.columns, img.rows, pixels)
    # img.write('grayscale.png')
  end
end
