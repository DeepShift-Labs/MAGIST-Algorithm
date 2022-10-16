use std::time::{Duration, Instant};


fn compute(n: f32, scale: f32, scalar: f32) -> f32 {
    let x = n * scale;
    let part1 = (n * x).sin();
	let part2 = (1.0/x).sin();
	((part1 * part2).abs()) * scalar
}

fn main() {
    let mut values = vec![];

    for i in 1..30 {
        let start = Instant::now();
        let out = compute(50.0, 0.1, 1.0);
        let duration = start.elapsed();

        values.push(duration);


        println!("Time elapsed in expensive_function() is: {:.10?}", duration);
        println!("Computed Values is: {:.50?}", out);
    }
    println!("{:.10?}", values)
}
