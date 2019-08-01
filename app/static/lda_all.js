const topics = [{
    "name": "topic 1",
    "keywords": ["release", "award", "actress", "music", "perform"]
},
{
    "name": "topic 2",
    "keywords": ["season", "school", "time", "award"]
},
{
    "name": "topic 3",
    "keywords": ["album", "award", "music", "release", "record"]
},
{
    "name": "topic 4",
    "keywords": ["episode", "actress", "live", "season", "drama"]
},
{
    "name": "topic 5",
    "keywords": ["fight", "football", "game", "world"]
},
{
    "name": "topic 6",
    "keywords": ["match", "team", "player", "season", "league"]
}
];

const badge_classes = ['badge-primary', 'badge-secondary', 'badge-success', 'badge-danger', 'badge-warning', 'badge-info']

function submit_resume() {
    const resume = $('#resume').val();

    const $spinner = $('.spinner');
    const $resultPanel = $('.prediction-result');

    $spinner.show();
    $resultPanel.hide();

    $.ajax({
        type: "POST",
        url: '/recommendations_lda',
        data: {
            resume: resume
        },
        dataType: 'json'
    }).then((response) => {
        $spinner.hide();

        result = response.result.map((entry) => {
            return {
                topic_id: entry.topic_id,
                score: parseFloat(entry.score)
            }
        })

        result.sort((a, b) => {
            return b.score - a.score;
        });

        mostPossible2 = result.length >= 2 ? [result[0], result[1]] : [result[0]];

        const $topic_ui_items = $('.topics .list-group-item');


        for (let topic_ui_item of $topic_ui_items) {
            $(topic_ui_item).removeClass('choosen');
        }

        for (let topic of mostPossible2){
            $('#result-topics').append(
                '<span class="badge ' + badge_classes[topic.topic_id] + '">topic ' + (topic.topic_id + 1) + '</span>'
            );

            $($topic_ui_items[topic.topic_id]).addClass('choosen');
        }

        console.log(result);
        $resultPanel.show();
    }, (error) => {
        $spinner.hide();
        $resultPanel.show();

        $('#result-topics').append(
            'there is an error processing the request' + error
        )
    });
}

$(document).ready(() => {

    const $all_topics = $('.topics');
    $all_topics.empty();

    let i = 0;

    for (let topic of topics){
        $all_topics.append(
            '<li class="list-group-item"><span class="badge ' + badge_classes[i] + '">' + topic.name + '</span> ('
             + topic.keywords.join(',')+')</li>'
        )

        i++;
    }

    $('.spinner').hide();
    $('.prediction-result').hide()
});