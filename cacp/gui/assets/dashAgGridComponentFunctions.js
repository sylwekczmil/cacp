var dashAgGridComponentFunctions = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dashAgGridComponentFunctions.Button = function (props) {
    const {setData, data} = props;
    console.log('xxx', props, data)

    function onClick() {
        setData();
    }

    return React.createElement(
        'i',
        {
            onClick: onClick,
            className: "bi bi-trash delete-button",
        },
        ''
    );
};
