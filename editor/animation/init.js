requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function fillingAnimation(tgt_node, data) {

            if (!data || !data.ext) {
                return
            }

            // hide right-answer
            $(tgt_node.parentNode).find(".answer").remove()

            const input = data.in
            const output = data.out
            const [error_msg, error_cells] = data.ext.result_addon

            /*----------------------------------------------*
             *
             * attr
             *
             *----------------------------------------------*/
            const attr = {
                outer_frame: {
                    'stroke-width': '2px',
                    'stroke': '#294270',
                },
                inner_grid: {
                    'stroke-width': '1px',
                    'stroke': '#82D1F5',
                },
                answer_grid: {
                    'stroke-width': '1px',
                    'stroke': '#294270',
                },
                number: {
                    input: {
                        'font-family': 'sans-serif',
                        'font-weight': 'bold',
                        'stroke-width': 0,
                        'fill': '#294270',
                    },
                    output: {
                        'font-family': 'sans-serif',
                        'font-weight': 'bold',
                        'stroke-width': 0,
                        'fill': '#8FC7ED',
                        'fill': '#577EC1',
                    },
                },
                error_cell: {
                    'stroke-width': '0px',
                    'stroke': '#294270',
                    'fill': '#FABA00',
                },
            }

            /*----------------------------------------------*
             *
             * values
             *
             *----------------------------------------------*/
            const grid_size_px = 300
            const os = 10
            const width = input[0].length
            const height = input.length
            const unit = grid_size_px / width

            /*----------------------------------------------*
             *
             * paper
             *
             *----------------------------------------------*/
            const paper = Raphael(tgt_node, grid_size_px+os*2, unit*height+os*2, 0, 0)

            /*----------------------------------------------*
             *
             * error_cells
             *
             *----------------------------------------------*/

            // error_cells
            error_cells.forEach(([y, x]) => {
                    paper.rect(x*unit+os, y*unit+os, unit, unit).attr(attr.error_cell)
            })

            /*----------------------------------------------*
             *
             * draw grid
             *
             *----------------------------------------------*/

            // outer frame
            paper.rect(os, os, grid_size_px, unit*height).attr(attr.outer_frame)

            // horizontal
            for (let i = 1; i < height; i += 1) {
                paper.path(['M', 0+os, i*unit+os, 'h', grid_size_px]).attr(attr.inner_grid)
            }

            // vertical
            for (let i = 1; i < width; i += 1) {
                paper.path(['M', i*unit+os, 0+os, 'v', unit*height]).attr(attr.inner_grid)
            }

            /*----------------------------------------------*
             *
             * input numbers
             *
             *----------------------------------------------*/
            for (let i = 0; i < height; i += 1) {
                for (let j = 0; j < width; j += 1) {
                    if (input[i][j] > 0) {
                        paper.text(
                            j*unit+unit/2+os,
                            i*unit+unit/2+os,
                            input[i][j]).attr(attr.number.input).attr(
                                {'font-size': 20*Math.max(0.3, unit/50)})
                    }
                }
            }

            /*----------------------------------------------*
             *
             * output numbers
             *
             *----------------------------------------------*/
            if (!(error_msg && error_cells.length == 0)) {
                for (let i = 0; i < height; i += 1) {
                    for (let j = 0; j < width; j += 1) {
                        if (output[i][j] > 0 && input[i][j] == 0) {
                            paper.text(
                                j*unit+unit/2+os,
                                i*unit+unit/2+os,
                                output[i][j]).attr(attr.number.output).attr(
                                    {'font-size': 20*Math.max(0.3, unit/50)})
                        }
                    }
                }
            }

            /*----------------------------------------------*
             *
             * draw vertical separator
             *
             *----------------------------------------------*/
            for (let y = 0; y < height; y += 1) {
                for (let x = 0; x < width - 1; x += 1) {

                    if (input[y][x] == 1 ||
                        input[y][x+1] == 1 ||
                        input[y][x] && input[y][x+1] && input[y][x] !== input[y][x+1]) {

                        paper.path(['M', (x+1)*unit+os, y*unit+os, 'v', unit]).attr(attr.answer_grid)
                    }

                    if (!(error_msg && error_cells.length == 0)) {
                        if (output[y][x] && output[y][x+1] && output[y][x] !== output[y][x+1]) {
                            paper.path(['M', (x+1)*unit+os, y*unit+os, 'v', unit]).attr(attr.answer_grid)
                        }
                    }
                }
            }

            /*----------------------------------------------*
             *
             * draw horizontal separator
             *
             *----------------------------------------------*/
            for (let x = 0; x < width; x += 1) {
                for (let y = 0; y < height - 1; y += 1) {

                    if (input[y][x] == 1 ||
                        input[y+1][x] == 1 ||
                        input[y][x] && input[y+1][x] && input[y][x] !== input[y+1][x]) {

                        paper.path(['M', (x)*unit+os, (y+1)*unit+os, 'h', unit]).attr(attr.answer_grid)
                    }

                    if (!(error_msg && error_cells.length == 0)) {
                        if (output[y][x] && output[y+1][x] && output[y][x] !== output[y+1][x]) {
                            paper.path(['M', (x)*unit+os, (y+1)*unit+os, 'h', unit]).attr(attr.answer_grid)
                        }
                    }
                }
            }

            /*----------------------------------------------*
             *
             * message
             *
             *----------------------------------------------*/
            if (!data.ext.result) {
                $(tgt_node).addClass('output').prepend(
                    '<div>' + error_msg+ '</div>').css(
                        {'border': '0','display': 'block',})
            }

        }

        var $tryit;
        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'filling',
                //js: 'filling'
            },
            animation: function($expl, data){
                fillingAnimation(
                    $expl[0],
                    data,
                );
            }
        });
        io.start();
    }
);
