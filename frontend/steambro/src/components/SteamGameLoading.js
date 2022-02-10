import React from "react";

function SteamGameLoading(Component) {
    return function SteamGameLoadingComponent({isLoading, ...props}) {
        if (!isLoading) return <Component {...props} />;
        return (
            <p>data loading...</p>
        )
    }
}

export default SteamGameLoading