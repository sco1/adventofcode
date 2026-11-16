use std::str::FromStr;

struct Present {
    length: u32,
    width: u32,
    height: u32,
}

impl Present {
    fn surface_area(&self) -> u32 {
        2 * (self.length * self.width + self.width * self.height + self.height * self.length)
    }

    fn smallest_side_area(&self) -> u32 {
        let areas = vec![
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        ];

        *areas.iter().min().unwrap()
    }

    fn volume(&self) -> u32 {
        self.length * self.width * self.height
    }

    fn smallest_perimeter(&self) -> u32 {
        let perimeters = vec![
            2 * (self.length + self.width),
            2 * (self.length + self.height),
            2 * (self.width + self.height),
        ];

        *perimeters.iter().min().unwrap()
    }

    fn wrapping_area(&self) -> u32 {
        self.surface_area() + self.smallest_side_area()
    }

    fn ribbon(&self) -> u32 {
        self.volume() + self.smallest_perimeter()
    }
}

#[derive(Debug)]
pub struct PresentParseError;

impl FromStr for Present {
    type Err = PresentParseError;

    // Parse raw present dimensions, assumed to be of the form `lxwxh`
    //
    // e.g. `2x3x4` or `1x1x10`
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let dims: Vec<_> = s.split_terminator('x').collect();

        let length = dims[0].parse().map_err(|_| PresentParseError)?;
        let width = dims[1].parse().map_err(|_| PresentParseError)?;
        let height = dims[2].parse().map_err(|_| PresentParseError)?;

        Ok(Present {
            length,
            width,
            height,
        })
    }
}

pub fn find_total_wrapping(presents: &str) -> u32 {
    presents
        .lines()
        .map(|line: &str| {
            let present: Present = line.parse().unwrap();
            present.wrapping_area()
        })
        .sum()
}

pub fn find_total_ribbon(presents: &str) -> u32 {
    presents
        .lines()
        .map(|line: &str| {
            let present: Present = line.parse().unwrap();
            present.ribbon()
        })
        .sum()
}
