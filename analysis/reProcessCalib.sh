#!/bin/sh
for run in 263 275 287 299 311 323 350 362 386 410 425 437 449 461 476 488 500 512; do python analysis/analyze_run_array_with_barRef.py -i /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS -o /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS/RESULTS -r ${run} --arrayCode 405 --applyCalib 0; done
for run in 467 479 491 503 266 278 290 302 314 326 353 365 389 413 428 440 452 464; do python analysis/analyze_run_array_with_barRef.py -i /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS -o /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS/RESULTS -r ${run} --arrayCode 406 --applyCalib 0; done
for run in 407 419 431 443 455 470 482 494 506 269 281 293 305 317 329 356 368 392 416; do python analysis/analyze_run_array_with_barRef.py -i /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS -o /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS/RESULTS -r ${run} --arrayCode 407 --applyCalib 0; done
for run in 347 359 383 407 422 434 446 458 473 485 497 509 272 284 296 308 320 332; do python analysis/analyze_run_array_with_barRef.py -i /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS -o /data/cmsdaq/LYSOMULTIARRAYNEWLAB4ARRAYS/RESULTS -r ${run} --arrayCode 408 --applyCalib 0; done
