extern crate xml_rpc;

use xml_rpc::{Fault, Server};
use std::net::{IpAddr, Ipv4Addr, SocketAddr};
use serde::{Serialize, Deserialize};

// #[derive(Clone, Debug, Serialize, Deserialize)]
// struct MoveRightParams {
//     pub point: Point,
//     pub m: i64,
// }
//
//
// #[derive(Clone, Debug, Serialize, Deserialize)]
// struct Point {
//     pub x: i64,
//     pub y: i64,
// }
//
// fn move_right(mut p: MoveRightParams) -> Result<Point, Fault> {
//     p.point.x += p.m;
//
//     Ok(p.point)
// }

#[derive(Clone, Debug, Serialize, Deserialize)]
struct PosEmbeddingInputs {
    pub n: f32,
    pub scale: f32,
    pub scalar: f32
}

fn compute(inputs: PosEmbeddingInputs) -> Result<f32, Fault> {
    let n = inputs.n;
    let scale = inputs.scale;
    let scalar = inputs.scalar;
    let x = n * scale;
    let part1 = (n * x).sin();
	let part2 = (1.0/x).sin();
	Ok(((part1 * part2).abs()) * scalar)
}

fn main() {
    let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);
    let mut server = Server::new();

    server.register_simple("pos_embedding", &compute);

    let bound_server = server.bind(&socket).unwrap();

    println!("Running server");
    bound_server.run();
}
//
// use std::time::{Duration, Instant};
// use rust_decimal::Decimal;
//
// fn compute(n: Decimal, scale: Decimal, scalar: Decimal) -> Decimal {
//     let x = n * scale;
//     let part1 = (n * x).sin();
// 	let part2 = (Decimal::new(10, 1)/x).sin();
// 	((part1 * part2).abs()) * scalar
//
// }
//
// fn main() {
//     let mut values = vec![];
//
//     for i in 1..30 {
//         let start = Instant::now();
//         let out = compute(Decimal::new(50, 0), Decimal::new(01, 1), Decimal::new(1, 0));
//         let duration = start.elapsed();
//
//         values.push(duration);
//
//
//         println!("Time elapsed in expensive_function() is: {:?}", duration);
//     }
//     println!("{:?}", values)
// }
