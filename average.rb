10.times { |k|
  puts k+1
  `rm output.txt`
  100.times do |i|
    `python km.py #{k+1} >> output.txt`
  end

  File.open("output.txt", "r") { |file|
    text = file.read
    numArray = []
    sum = 0
    for line in text.split(/\R/)
      sum += line.to_f
      numArray.push(line.to_f)
    end
    puts sum/text.split(/\R/).length
    puts numArray.max
    puts numArray.min
  }
}

